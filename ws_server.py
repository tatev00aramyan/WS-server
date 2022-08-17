import websockets
import asyncio
import datetime


async def handler(websocket, path):
    print("A client just connected")
    try:
        while True:
            await websocket.send(str(datetime.now()))
            print(str(datetime.now()))
            await asyncio.sleep(2)
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")


if __name__ == "__main__":
    PORT = 8080
    start_server = websockets.serve(handler, "localhost", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
