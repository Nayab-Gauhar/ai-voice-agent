import asyncio
import websockets


async def main():

    async with websockets.connect(
        "ws://127.0.0.1:8000/ws"
    ) as websocket:

        print("Connected!")
        print("Type messages. Type 'exit' to quit.")

        while True:

            message = input("You: ")

            if message.lower() == "exit":
                break

            await websocket.send(message)

            response = await websocket.recv()

            print("Server:", response)


asyncio.run(main())