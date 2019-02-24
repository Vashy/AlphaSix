import unittest
from Butterfly.butterfly.consumer import KafkaConsumer

class TestConsumer(unittest.TestCase):
    def test_consumer(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092')
        consumer.subscribe(['test1', 'test2'])
        topiclist = consumer.subscription()

        self.assertIn('test1', topiclist)
        self.assertIn('test2', topiclist)

if __name__ == '__main__':
    unittest.main()
