from confluent_kafka import Consumer
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json


def main():
    while True:
        msg=c.poll(0.1) #timeout
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data=msg.value().decode('utf-8')
        data_json = json.loads(data)
        print(data_json)
        # data.append((data_json['Time'], float(data_json['Open Price'])))

        x_values.append(data_json['Time'])
        y_values.append(float(data_json['Open Price']))

        backview = len(x_values) if len(x_values) < 10 else 10
        ax.plot(x_values[-backview:], y_values[-backview:])
        plt.draw()
        plt.pause(0.01)
        plt.cla()

    c.close()

if __name__ == "__main__":
    c = Consumer(
        {'bootstrap.servers': 'localhost:9092', 'group.id': 'python-consumer', 'auto.offset.reset': 'earliest'})
    print('Kafka Consumer has been initiated...')

    print('Available topics to consume: ', c.list_topics().topics)
    c.subscribe(['crypto-open-price1'])

    x_values = []
    y_values = []
    fig, ax = plt.subplots()
    plt.xlabel("DateTime")
    plt.ylabel("Open Price")


    main()