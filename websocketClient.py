import asyncio
import websockets

async def connect():
    async with websockets.connect("ws://localhost:5000/WebSocketExample/websocket") as websocket:
        for i in range(1, 10, 1):
            await websocket.send("/index.html");
            data =await websocket.recv();
            print(data);
asyncio.get_event_loop().run_until_complete(connect())