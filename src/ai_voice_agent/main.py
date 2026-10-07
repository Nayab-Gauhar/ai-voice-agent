from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from ai_voice_agent.agent import get_ai_message
import os
import json
#loading the env
from dotenv import load_dotenv
load_dotenv()
BASE_URL = os.getenv("NGROK_URL")
WSS_URL = BASE_URL.replace("https://","wss://")
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

    try:
        while True:

            message = await websocket.receive_text()

            print("Browser:", message)

            await websocket.send_text(
                f"Server received: {message}"
            )

    except WebSocketDisconnect:
        print("Browser disconnected")