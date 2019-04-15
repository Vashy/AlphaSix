"""
File: test_mongousers.py
Data creazione: 2019-04-01

<descrizione>

Licenza: Apache 2.0

Copyright 2019 AlphaSix

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Versione: 0.2.1
Creatore: Timoty Granziero, timoty.granziero@gmail.com
"""

import unittest
from mongo_db.singleton import MongoSingleton
from mongo_db.users import MongoUsers


class TestMongoUsers(unittest.TestCase):

    # Chiamato all'inizio
    @classmethod
    def setUpClass(cls):  # NOSONAR
        cls.client = MongoUsers(MongoSingleton.Singleton('butterfly_test'))

    # Chiamato alla fine
    @classmethod
    def tearDownClass(cls):  # NOSONAR
        cls.client._mongo._client.drop_database('butterfly_test')

    def test_crud(self):
        with self.subTest('Raises'):
            self.assertRaises(
                AssertionError,  # Ne telegram ne email inseriti
                self.client.create,
                name='Timoty',
                surname='Granziero',
            )

        with self.subTest('Create'):
            res = self.client.create(
                _id=123,
                name='Timoty',
                surname='Granziero',
                telegram='12332').inserted_id
            assert res == 123

            res = self.client.create(
                _id=124,
                name='Simone',
                surname='Granziero',
                telegram='12343',
                email='aa@a.it').inserted_id
            assert res == 124

            self.assertRaises(
                AssertionError,
                self.client.create,
                telegram='12343',
            )

            self.assertRaises(
                AssertionError,
                self.client.create,
                email='aa@a.it',
            )

        with self.subTest('Read'):
            self.assertRaises(
                AssertionError,  # Nessun contatto TG o email corrispondente
                self.client.read,
                'aaa'
            )
            user = self.client.read('12332')
            assert user['name'] == 'Timoty'
            assert user['surname'] == 'Granziero'
            assert user['email'] is None

            user = self.client.read('aa@a.it')
            assert user['name'] == 'Simone'
            assert user['surname'] == 'Granziero'
            assert user['telegram'] == '12343'
            assert user['email'] is not None

        with self.subTest('Update name'):
            self.assertRaises(
                AssertionError,  # Nessun contatto TG o email corrispondente
                self.client.update_name,
                'aaa',
                'New name',
            )

            user = self.client.read('12343')
            assert user['name'] != 'Andrew'

            res = self.client.update_name('12343', 'Andrew')
            assert res['name'] == 'Simone'  # ex name

            user = self.client.read('12343')
            assert user['name'] == 'Andrew'

        with self.subTest('Update surname'):
            self.assertRaises(
                AssertionError,  # Nessun contatto TG o email corrispondente
                self.client.update_surname,
                'aaa',
                'New surname',
            )

            user = self.client.read('12343')
            assert user['surname'] != 'Tanenbaum'

            res = self.client.update_surname('12343', 'Tanenbaum')
            assert res['surname'] == 'Granziero'  # ex name

            user = self.client.read('12343')
            assert user['surname'] == 'Tanenbaum'

        with self.subTest('Update Telegram'):
            self.assertRaises(
                AssertionError,  # Nessun contatto TG o email corrispondente
                self.client.update_telegram,
                'aaa',
                'New telegram',
            )

            self.assertRaises(
                AssertionError,  # Contatto TG già presente
                self.client.update_telegram,
                '12343',
                '12332',
            )

            user = self.client.read('12343')
            assert user['telegram'] == '12343'
            assert user['name'] == 'Andrew'

            res = self.client.update_telegram('12343', '12345')
            assert res['telegram'] == '12343'

            user = self.client.read('12345')
            assert user['telegram'] == '12345'
            assert user['name'] == 'Andrew'
            assert user['surname'] == 'Tanenbaum'

        with self.subTest('Update email'):
            self.assertRaises(
                AssertionError,  # Nessun contatto TG o email corrispondente
                self.client.update_email,
                'aaa',
                'eee@email.it',
            )

            self.assertRaises(
                AssertionError,  # Contatto email già presente
                self.client.update_email,
                '12345',
                'aa@a.it',
            )

            user = self.client.read('12345')
            assert user['email'] == 'aa@a.it'
            assert user['name'] == 'Andrew'

            res = self.client.update_email('12345', 'aa@email.it')
            assert res['email'] == 'aa@a.it'

            user = self.client.read('12345')
            assert user['telegram'] == '12345'
            assert user['name'] == 'Andrew'
            assert user['surname'] == 'Tanenbaum'
            assert user['email'] == 'aa@email.it'


        with self.subTest('Delete'):
            res = self.client.delete_from_id(123).deleted_count
            assert res == 1

            # Failed delete
            res = self.client.delete('aaa@a.it').deleted_count
            assert res == 0

            res = self.client.delete('aa@email.it').deleted_count
            assert res == 1

    def test_match_labels_issue(self):
        assert self.client.match_labels_issue(
            [1, 2, 4],
            [4, 5, 6],
        ) is True
        assert self.client.match_labels_issue(
            [4],
            ['str', 'aaa', 'b', 4],
        ) is True
        assert self.client.match_labels_issue(
            [1, 2, 3, 16],
            [4, 5, 6],
        ) is False
        assert self.client.match_labels_issue(
            [1, 2, 3, 16],
            [],
        ) is False
        assert self.client.match_labels_issue(
            [],
            [1, 2, 3, 16],
        ) is False

    def test_match_keyword_commit(self):
        assert self.client.match_keyword_commit(
            ['CI', 'java'],
            'Stringa contenente CI.',
        ) is True
        assert self.client.match_keyword_commit(
            ['CI', 'java'],
            'Stringa non contenente keywords. JAVA case sensitive',
        ) is False
        assert self.client.match_keyword_commit(
            ['CI', 'java'],
            'Stringa non contenente keywords. JAVA case insensitive',
            case=False,
        ) is True

    def test_add_labels(self):
        res = self.client.create(
            _id=1000,
            name='Timoty',
            surname='Granziero',
            telegram='111').inserted_id
        assert res == 1000

        self.client.add_labels('111', 'PROJECT', 'label1', 'label2')

        user = self.client.read('111')
        assert user['surname'] == 'Granziero'
        assert 'label1' in user['projects'][0]['topics']
