import websockets
import asyncio
from pyngrok import ngrok
from ra_dec_app import run


async def handler(websocket):
    print("A client just connected")
    try:
        while True:
            ra, dec = run()
            ra_dec = f"RA: {ra}, DEC:{dec}"
            await websocket.send(ra_dec)
            print(ra_dec)
            await asyncio.sleep(10)
    except websockets.ConnectionClosed:
        print("A client just disconnected")


def run_server():
    port = 8080
    http_tunnel = ngrok.connect(port, bind_tls=True)
    print("testing url is: ", http_tunnel.public_url)
    start_server = websockets.serve(handler, "localhost", port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    run_server()
