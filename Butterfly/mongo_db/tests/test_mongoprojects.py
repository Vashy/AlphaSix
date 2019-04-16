"""
File: test_mongoprojects.py
Data creazione: 2019-04-02

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
import datetime

import pytest

from mongo_db.singleton import MongoSingleton
from mongo_db.projects import MongoProjects


class TestMongoProjects(unittest.TestCase):

    # Chiamato all'inizio
    @classmethod
    def setUpClass(cls):  # NOSONAR
        cls.client = MongoProjects(MongoSingleton.Singleton('butterfly_test'))

    # Chiamato alla fine
    @classmethod
    def tearDownClass(cls):  # NOSONAR
        cls.client._mongo._client.drop_database('butterfly_test')

    def test_crud(self):  # NOSONAR
        with self.subTest('Create'):
            res = self.client.create(
                _id=10,
                url='http://project',  # url
                name='Project',  # name
                app='gitlab',  # app
                topics=[
                    1, 2, 'abc',
                ],  # topics
            )
            assert res.inserted_id == 10
            res = self.client.collection.find({'url': 'http://project'}).next()
            assert res['app'] == 'gitlab'
            assert 1 in res['topics']
            assert 2 in res['topics']
            assert 'abc' in res['topics']

            self.assertRaises(  # Progetto già esistente
                AssertionError,
                self.client.create,
                _id=11,
                url='http://project',  # url
                name='Project',  # name
                app='gitlab',  # app
                topics=[
                    1, 2, 'abc',
                ],  # topics
            )

            self.assertRaises(  # Trailing slash
                AssertionError,
                self.client.create,
                _id=15,
                url='http://project/',  # url
                name='Project',  # name
                app='gitlab',  # app
                topics=[
                    1, 2, 'abc',
                ],  # topics
            )
            self.assertRaises(  # url non assegnato
                AssertionError,
                self.client.create,
                _id=12,
                name='Project',  # name
                app='gitlab',  # app
                topics=[
                    1, 2, 'abc',
                ],  # topics
            )

            self.assertRaises(  # app non assegnata
                AssertionError,
                self.client.create,
                _id=13,
                url='http://project23',  # url
                name='Project',  # name
                topics=[
                    1, 2, 'abc',
                ],  # topics
            )
            self.assertRaises(  # valore app sbagliato
                AssertionError,
                self.client.create,
                _id=13,
                url='http://project23',  # url
                app='gitlabs',
                name='Project',  # name
                topics=[
                    1, 2, 'abc',
                ],  # topics
            )

            self.assertRaises(  # campo non riconosciuto
                AssertionError,
                self.client.create,
                _id=13,
                url='http://project23',  # url
                name='Project',  # name
                naame='Campo non riconosciuto',
                topics=[
                    1, 2, 'abc',
                ],  # topics
            )

        with self.subTest('Delete'):
            res = self.client.delete('http://project')  # eliminazione per url
            assert res.deleted_count == 1
            res = self.client.delete('http://projects')  # eliminazione per url
            assert res.deleted_count == 0

            res = self.client.create(
                _id=12,
                url='http://project',  # url
                name='Project',  # name
                app='gitlab',  # app
                topics=[
                    1, 2, 'abc',
                ],  # topics
            )
            assert res.inserted_id == 12
            res = self.client.delete(12)
            assert res.deleted_count == 1

    def test_update_app(self):
        res = self.client.create(
                _id=15,
                url='http://project1',  # url
                name='Project',  # name
                app='gitlab',  # app
                topics=[
                    1, 2, 'abc',
                ],  # topics
            )
        project = self.client.read(15)
        assert project['url'] == 'http://project1'
        assert project['app'] == 'gitlab'

        self.client.update_app('http://project1', 'redmine')
        project = self.client.read(15)
        assert project['app'] == 'redmine'

        self.assertRaises(  # app non riconosciuta
            AssertionError,
            self.client.update_app,
            'http://project1',
            'redmane',
        )

        self.assertRaises(  # Progetto inesistente
            AssertionError,
            self.client.update_app,
            'httpsss://project1',
            'redmane',
        )
