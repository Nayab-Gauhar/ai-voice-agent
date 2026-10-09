import asyncio
import json
import os
from dotenv import load_dotenv
import websockets
load_dotenv()

DEEPGRAM_API_KEY = os.environ["DEEPGRAM_API_KEY"]


async def connect_to_deepgram():
    url = (
        "wss://api.deepgram.com/v1/listen"
        "?model=nova-3"
        "&interim_results=true"
        "&endpointing=300"
        "&punctuate=true"
        "&vad_events=true"
    )

    deepgram_ws = await websockets.connect(
        url,
        additional_headers={
            "Authorization": f"Token {DEEPGRAM_API_KEY}"
        },
        ping_timeout=60,
    )

    print("Connected to Deepgram")

    return deepgram_ws