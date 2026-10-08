from pathlib import Path
from ai_voice_agent.speech.stt import connect_to_deepgram
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from ai_voice_agent.agent import get_ai_message
import os
import json
#loading the env
import asyncio
from dotenv import load_dotenv
load_dotenv()
# BASE_URL = os.getenv("NGROK_URL")
# WSS_URL = BASE_URL.replace("https://","wss://")
BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"

app = FastAPI(
    title="Gmail Calling Agent",
    description="AI Agent voice assistant with Gmail Integrations",
    version="0.1.0",
)

app.mount(
    "/static",
    StaticFiles(directory=WEB_DIR),
    name="static",
)

@app.get("/")
async def home():
    return FileResponse(WEB_DIR / "index.html")

@app.get('/health')
async def health():
    return{
        "status":"healthy"
    }

@app.post('/test')
async def test(data:UserMessage):
    return{
        "message" : data.message,
        "status" : "success"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    print("Browser Connected")

    deepgram_ws = None

    try:
        while True:

            deepgram_ws = await connect_to_deepgram()

            browser_to_deepgram = asyncio.create_task(forward_audio(websocket,deepgram_ws))

            deepgram_to_browser = asyncio.create_task(forward_transcript(websocket,deepgram_ws))

            await asyncio.gather(browser_to_deepgram,deepgram_to_browser)

    except Exception as e:
        print("Error Occured",e)

    finally:
        if deepgram_ws:
            await deepgram_ws.close()

            print("Connection closed")    
    
async def forward_audio(browser_ws,deepgram_ws):
    while True:

        audio_data = await browser_ws.receive_bytes()

        print("Browser to Deeprtgam is giving",len(audio_data),"bytes")

        await deepgram_ws.send(audio_data)

    
async def forward_transcript(browser_ws, deepgram_ws):
    utterance_buffer = []

    async for message in deepgram_ws:

        data = json.loads(message)

        print("Deepgram:", data)

        #for getting the transcription
        if data.get("type") != "Results":
            continue

        channel = data.get("channel", {})
        alternatives = channel.get("alternatives", [])

        if not alternatives:
            continue

        transcript = alternatives[0].get("transcript", "")

        if not transcript:
            continue

        is_final = data.get("is_final",False)
        speech_final = data.get("speech_final",False)

        #interim resuklt we have to capture
        if not is_final:
            await browser_ws.send_text(
                json.dumps({
                    "type":"transcript",
                    "text":transcript,
                    "is_final":False,
                    "speech_final":False,
                })
            )
            continue
        
        #final segment
        utterance_buffer.append(transcript)

        print(f"Transcript : {utterance_buffer}")

        #storing the final values 

        if speech_final:
            complete_utterance = " ".join(utterance_buffer)

            print("Speech :",complete_utterance)

            await browser_ws.send_text(
                json.dumps({
                    "type":"transcript",
                    "text":complete_utterance,
                    "is_final":True,
                    "speech_final":True,

                })
            )
            #gemini ko bhej rahe hain
            ai_response = await asyncio.to_thread(get_ai_message,complete_utterance)

            print("Ai Rponse :",ai_response)

            #send gemini data to browser

            await browser_ws.send_text(
                json.dumps({
                    "type":"ai_response",
                    "text":ai_response,
                })
            )
            #after displaying clear it
            utterance_buffer.clear()
        else:
            await browser_ws.send_text(
                json.dumps({
                    "type":"transcript",
                    "text":transcript,
                    "is_final":True,
                    "speech_final":False,

                })
            )
