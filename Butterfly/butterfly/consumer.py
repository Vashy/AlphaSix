import sys
from kafka import KafkaConsumer
import kafka.errors
from abc import ABC, abstractmethod
import configparser

class Consumer(object):
    pass

if __name__ == "__main__":
    # consumer = KafkaConsumer(bootstrap_servers='localhost:9092')
    # # print(consumer.topics())
    # consumer.subscribe(['test', 'gitlab'])
    # # print(consumer.subscription())

    # consumer.seek_to_beginning()

    # consumer.close()

    consumer = KafkaConsumer(
        'test',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
    )

    for message in consumer:
        message = message.value.decode()
        print(message)
