from confluent_kafka import Producer
import websocket
import json
import datetime
import threading
import pandas as pd
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import logging
import numpy as np


logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

p=Producer({'bootstrap.servers':'localhost:9092'})
print('Kafka Producer has been initiated...')


def create_df(data) -> pd.DataFrame:
    return pd.DataFrame(data)


def receipt(err,msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)


def on_message(ws, message):
    # Define how to handle incoming messages
    # print("Received message:", message)
    message = json.loads(message)
    # You can process the received data here based on your requirements
    if "E" in message and "o" in message:
        timestamp = message['E'] / 1000
        timestamp = datetime.datetime.utcfromtimestamp(timestamp)
        print(f"Time: {timestamp}, Open Price: {message['o']}")

        data = {
            'Time': str(timestamp),
            'Open Price': message['o']
        }
        m=json.dumps(data)
        p.poll(1)
        p.produce('crypto-open-price1', m.encode('utf-8'), callback=receipt)
        p.flush()
        time.sleep(3)


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
    ws.run_forever()






if __name__ == "__main__":
    global data
    global df
    data = []


    duration = 300
    # Start the WebSocket connection
    websocket_thread = threading.Thread(target=open_websocket)
    websocket_thread.start()

    # Set the timer to close the WebSocket after 5 seconds
    timer_thread = threading.Timer(duration, close_websocket)
    timer_thread.start()



