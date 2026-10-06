import asyncio
import socket
import websockets


async def main():

    async with websockets.connect(
        "wss://reformist-jubilant-creole.ngrok-free.dev/ws",
        proxy=None,
        # family=socket.AF_INET,
    ) as websocket:

        print("Connected!")

        await websocket.send("Hello")

        response = await websocket.recv()

        print("Server:", response)


asyncio.run(main())