#!/usr/bin/env python3

# Uso: python3 path/to/consumer.py

# from kafka import KafkaConsumer
# import kafka.errors
from abc import ABC, abstractmethod
# import json
# from pathlib import Path

class Consumer(ABC):
    """Interfaccia Consumer"""

    @abstractmethod
    def listen(self):
        """Resta in ascolto del Broker"""
        pass

