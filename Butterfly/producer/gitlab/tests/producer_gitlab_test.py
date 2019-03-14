import unittest
from producer.gitlab import GLProducer
# Scrivere da Butterfly il percorso con . non /

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    # def test_    


if __name__ == '__main__':
    unittest.main()