import asyncio
import json

from websockets import client
from websockets.exceptions import ConnectionClosed

async def attach_2_bitmex(instrument: str) -> None:
    """Attach to the bitmex api and stream incoming trades"""
    uri = "wss://www.bitmex.com/realtime"
    async with client.connect(uri) as websocket:
        # Send a message to subscribe to XBTUSD updates
        msg = {"op": "subscribe", "args": [f"instrument:{instrument}"]}
        await websocket.send(json.dumps(msg))
        # Receive messages in a loop and print them out
        while True:
            try:
                result = await websocket.recv()
                data = json.loads(result)
                # print(data)
                extract_load_price(data)
                print("-----------------")
            except ConnectionClosed:
                break

            # Add a delay to prevent the function from exiting immediately
        await asyncio.sleep(1)


async def runner(instrument: str = "XBTUSD") -> None:
    task1 = asyncio.create_task(attach_2_bitmex(instrument))
    await task1


def extract_load_price(json_output: dict) -> None:
    if "data" in json_output:
        for i in json_output['data']:
            if 'lastPrice' in i:
                print(i['lastPrice'])

if __name__ == "__main__":
    asyncio.run(runner())