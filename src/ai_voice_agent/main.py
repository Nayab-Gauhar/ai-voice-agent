from fastapi import FastAPI,Request
from pydantic import BaseModel,Field
from typing import Annotated
from fastapi.responses import Response
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

    twiml = """
    <Response>
        <Say>Hello! Kya re madarchod kya kr raha hai.</Say>
    </Response>
    """

    return Response(
        content=twiml,
        media_type="application/xml"
    )