import websocket
import json
import datetime
import threading
import pandas as pd
import matplotlib.pyplot as plt

# class DataHolder:
#     def __init__(self, data):
#         self.df = None
#         self.data = data
#
#     def update_dataframe(self, new_data):
#         # Update the DataFrame with new data
#         # ...
#
#     def get_dataframe(self):
#         return pd.DataFrame(data)

def append_df(df: pd.DataFrame, data: dict) -> pd.DataFrame:
    df.append(df, data)

def create_df(data) -> pd.DataFrame:
    df = pd.DataFrame(data)
    return df

def on_message(ws, message):
    # Define how to handle incoming messages
    # print("Received message:", message)
    message = json.loads(message)
    # You can process the received data here based on your requirements
    if "E" in message and "o" in message:
        timestamp = message['E'] / 1000
        timestamp = datetime.datetime.utcfromtimestamp(timestamp)
        print(f"Time: {timestamp}, Open Price: {message['o']}")
        data.append({"Timestamp": timestamp, "Open Price": message['o']})

def on_error(ws, error):
    # Define how to handle WebSocket errors
    print("WebSocket error:", error)

def on_close(ws, close_code, close_reason):
    # Define how to handle WebSocket connection closure
    print("WebSocket connection closed")
    df = pd.DataFrame(data)
    print(df)

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
        ws.close()

def run_websocket():
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
    ws.run_forever()


if __name__ == "__main__":
    global data
    data = []
    # data_holder = DataHolder()

    # Start the WebSocket connection
    websocket_thread = threading.Thread(target=run_websocket)
    websocket_thread.start()

    # Set the timer to close the WebSocket after 5 seconds
    timer_thread = threading.Timer(4, close_websocket)
    timer_thread.start()
