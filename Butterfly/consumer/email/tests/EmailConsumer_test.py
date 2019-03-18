import json
import unittest
from pathlib import Path


class TelegramConsumerTest(unittest.TestCase):

    # def test_constructor(self):
        # lst = ['bug', 'fix', 'enhancement']
        # with open(Path(__file__).parents[2] / 'config.json') as f:
        #    config = json.load(f)
        # print(config)
        # prova = EmailConsumer.EmailConsumer(lst, config)
        # assert isinstance(prova, KafkaConsumer)

    def test_pretty(self):
        with open(Path(__file__).parents[0] / 'test.json') as f:
            obj = json.load(f)
        res = "".join(
            [
                f'*Provenienza*: {obj["type"]}'
                '\n\n*È stata aperta una issue nel progetto*: '
                f'{obj["project_name"]} ',
                f'({obj["project_id"]})',
                f'\n\n*Author*: {obj["author"]}'
                '\n\n *Issue\'s information: *'
                f'\n - *Title*: \t\t{obj["title"]}',
                f'\n - *Description*: \t\t{obj["description"]}',
                f'\n - *Action*: \t{obj["action"]}',
                '\n\n*Assegnee\'s information:*'
            ]
        )
        prova = "".join(
            [
                f'*Provenienza*: GL'
                '\n\n*È stata aperta una issue nel progetto*: prova (01)',
                f'\n\n*Author*: pippo'
                '\n\n *Issue\'s information: *'
                f'\n - *Title*: \t\tbutterfly',
                f'\n - *Description*: \t\tdescrizione',
                f'\n - *Action*: \tazione',
                '\n\n*Assegnee\'s information:*'
            ]
        )
        self.assertEqual(res, prova)


if __name__ == '__main__':
    unittest.main()
