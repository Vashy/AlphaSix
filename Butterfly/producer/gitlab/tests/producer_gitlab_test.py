import unittest
import json
from pathlib import Path
from producer.gitlab import GLProducer
from kafka import KafkaProducer
import kafka.errors
# Scrivere da Butterfly il percorso con . non /

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
    
    #PRE: deve girare Kafka
    def test_GLProducer_constructor(self):
        print(Path(__file__).parents[2]/'config.json')
        with open(Path(__file__).parents[2]/'config.json') as f:
            config = json.load(f)
        kafkaObject = GLProducer.GLProducer(config['kafka'])
        self.assertIsInstance(kafkaObject , KafkaProducer)




if __name__ == '__main__':
    unittest.main()