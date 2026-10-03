from fastapi import FastAPI,Request
from pydantic import BaseModel,Field
from typing import Annotated
from fastapi.responses import Response
import os
#loading the env
from dotenv import load_dotenv
load_dotenv()
BASE_URL = os.getenv("NGROK_URL")

app = FastAPI(
    title="Gmail Calling Agent",
    description="AI Agent voice assistant with Gmail Integrations",
    version="0.1.0",
)

class UserMessage(BaseModel):
    message : str



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

    form_data = await request.form()

    caller = form_data.get("From")
    call_sid = form_data.get("CallSid")

    print(f"Incoming call from: {caller}")
    print(f"Call SID: {call_sid}")
    print(dict(form_data))

    twiml = f"""
    <Response>
        <Gather
            input="speech"
            action="{BASE_URL}/process-speech"
            method="POST"
            language="en-IN"
            speechTimeout="3"
        >
            <Say>Hello! How can I help you?</Say>
        </Gather>
            <Say>
                I didn't hear anything. Goodbye.
            </Say>
    </Response>
    """

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

    twiml = f"""
    <Response>
        <Say>
            You said: {speech_result}
        </Say>
    </Response>
    """

    return Response(
        content=twiml,
        media_type="application/xml"
    )