from fastapi import FastAPI,Request,WebSocket,WebSocketDisconnect
from pydantic import BaseModel,Field
from typing import Annotated
from fastapi.responses import Response
from html import escape
from ai_voice_agent.agent import get_ai_message
import os
import json
#loading the env
from dotenv import load_dotenv
load_dotenv()
import asyncio
BASE_URL = os.getenv("NGROK_URL")
WSS_URL = BASE_URL.replace("https://","wss://")


app = FastAPI(
    title="Gmail Calling Agent",
    description="AI Agent voice assistant with Gmail Integrations",
    version="0.1.0",
)

class UserMessage(BaseModel):
    message : str

def conversation_gather():
    return f""""
    <Gather input="speech" action="{BASE_URL}/process-speech" method="POST" speechTimeout="auto">
    </Gather>
    <Say> I didn't hear you anything? </Say>
    <Redirect>{BASE_URL}/voice</Redirect>
    """
 
@app.get('/')
async def home():
    return {"message":"AI Voice Agent is running!!"}

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

@app.post("/voice")
async def voice(request: Request):

    twiml = f"""
    <Response>
        <Say>WebSocket test started. You can speak now.</Say>
        <Connect>
            <Stream url="{WSS_URL}/ws" />
        </Connect>
    </Response>
    """

    print("TwiML being sent:")
    print(twiml)

    return Response(
        content=twiml,
        media_type="application/xml"
    )


@app.post("/process-speech")
async def process_speech(request: Request):

    form_data = await request.form()

    speech_result = form_data.get("SpeechResult")
    confidence = form_data.get("Confidence")

    print(f"User Spoken: {speech_result}")
    print(f"Confidence: {confidence}")
    if not speech_result:
        response_text = "Sorry I didn't hear it."
    else:
        response_text = get_ai_message(speech_result)
    print(f"AI Message : {response_text}")
    safe_speech_for_xml = escape(response_text)
    twiml = f"""
    <Response>
        <Say>
            {safe_speech_for_xml}
        </Say>
        {conversation_gather()}
    </Response>
    """

    return Response(
        content=twiml,
        media_type="application/xml"
    )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    print("✅ WebSocket connected")

    try:
        while True:

            message = await websocket.receive_text()

            print("Client:", message)

            await websocket.send_text(
                f"Server received: {message}"
            )

    except WebSocketDisconnect:

        print("❌ WebSocket disconnected")