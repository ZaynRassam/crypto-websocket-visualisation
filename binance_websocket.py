import websocket
import json
import datetime
import threading
import pandas as pd
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def create_df(data) -> pd.DataFrame:
    return pd.DataFrame(data)

def on_message(ws, message):
    # Define how to handle incoming messages
    # print("Received message:", message)
    message = json.loads(message)
    # You can process the received data here based on your requirements
    if "E" in message and "o" in message:
        timestamp = message['E'] / 1000
        # timestamp = datetime.datetime.utcfromtimestamp(timestamp)
        print(f"Time: {timestamp}, Open Price: {message['o']}")
        data.append((timestamp, float(message['o'])))

def on_error(ws, error):
    # Define how to handle WebSocket errors
    print("WebSocket error:", error)

def on_close(ws, close_code, close_reason):
    # Define how to handle WebSocket connection closure
    print("WebSocket connection closed")
    global df
    df = create_df(data)

def on_open(ws):
    # Define actions to be taken when the WebSocket connection is opened
    print("WebSocket connection opened")
    # Send a subscription message to subscribe to a data stream
    subscription_message = {
        "method": "SUBSCRIBE",
        "params": [
            "btcusdt@miniTicker"  # Example: Subscribe to BTC/USDT trades
        ],
        "id": 1
    }
    ws.send(json.dumps(subscription_message))

def close_websocket():
    if ws:
        print("Closing connection")
        ws.close()
        global websocket_running
        websocket_running = False
    else:
        print("Could not close connection")

def open_websocket():
    # Define the WebSocket endpoint URL
    websocket_url = "wss://stream.binance.com:9443/ws"

    # Create a WebSocket connection
    global ws
    ws = websocket.WebSocketApp(websocket_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    # Run the WebSocket connection
    global websocket_running
    websocket_running = True
    ws.run_forever()


def animate(i):
    ax.relim()
    ax.autoscale_view()
    line.set_data(*zip(*data))



if __name__ == "__main__":
    global data
    global df
    global websocket_running
    websocket_running = True
    data = []
    # data_holder = DataHolder()

    duration = 300
    # Start the WebSocket connection
    websocket_thread = threading.Thread(target=open_websocket)
    websocket_thread.start()

    # Set the timer to close the WebSocket after 5 seconds
    timer_thread = threading.Timer(duration, close_websocket)
    timer_thread.start()

    fig, ax = plt.subplots()
    x=None
    y=None
    data = deque([(x, y)], maxlen=20)
    line, = plt.plot(*zip(*data), c='black')
    plt.ylabel("Open Price")
    plt.xlabel("Time since epoch")

    ani = animation.FuncAnimation(fig, animate, interval=100)
    plt.show()

    while websocket_running:
        pass


    print("Finished")

