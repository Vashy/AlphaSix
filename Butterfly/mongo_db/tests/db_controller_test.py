import unittest
from mongo_db.db_controller import DBConnection, DBController


class TestDBController(unittest.TestCase):

    # Chiamato all'inizio
    @classmethod
    def setUpClass(cls):
        cls.client = DBConnection('butterfly')
        cls.controller = DBController(cls.client, False)

    # Chiamato alla fine
    @classmethod
    def tearDownClass(cls):
        cls.client.close()

    def test_db_instances(self):
        collection = self.client.db.users
        # Cerca un documento qualsiasi
        self.assertIsNotNone(collection.find_one({}))

        self.assertIsNotNone(collection.find_one({'_id': 1}))
        self.assertIsNotNone(collection.find_one({'_id': 2}))
        self.assertIsNotNone(collection.find_one({'_id': 3}))

        timoty = collection.find_one({'name': 'Timoty'})
        self.assertIsNotNone(timoty)
        self.assertEqual(timoty['name'], 'Timoty')
        self.assertEqual(timoty['surname'], 'Granziero')
        self.assertEqual(timoty['sostituto'], 2)
        self.assertEqual(timoty['telegram'], '@user1')
        self.assertEqual(timoty['preferenza'], 'telegram')
        self.assertIsNone(timoty['email'])
        self.assertIn('mongodb', timoty['keywords'])
        self.assertIn('python', timoty['keywords'])
        self.assertIn('test', timoty['keywords'])

        simone = collection.find_one({
            'surname': 'Granziero',  # La virgola sottointende AND
            'topics': {
                '$size': 2  # Matcha array topics di dimensione 2
            }}
        )
        self.assertIsNotNone(simone)
        self.assertEqual(simone['name'], 'Simone')
        self.assertEqual(simone['surname'], 'Granziero')
        self.assertEqual(simone['sostituto'], 1)
        self.assertEqual(simone['telegram'], '@user2')
        self.assertEqual(simone['email'], 'simone.granziero@gmail.com')
        self.assertEqual(simone['preferenza'], 'email')
        self.assertGreaterEqual(len(simone['irreperibilità']), 3)
        self.assertGreaterEqual(len(simone['keywords']), 2)
        self.assertIn('2019-07-17', simone['irreperibilità'])
        self.assertEqual(simone['sostituto'], 1)

        mattia = collection.find_one({
            'name': 'Mattia',
            'surname': 'Ridolfi',
        })

        self.assertIsNotNone(mattia)
        self.assertEqual(mattia['name'], 'Mattia')
        self.assertEqual(mattia['surname'], 'Ridolfi')
        self.assertEqual(mattia['sostituto'], 1)
        self.assertEqual(mattia['preferenza'], 'email')
        self.assertEqual(mattia['email'], 'mattia.ridolfi@gmail.com')
        self.assertIsNone(mattia['telegram'])
        self.assertGreaterEqual(len(mattia['keywords']), 2)
        self.assertGreaterEqual(len(mattia['topics']), 0)

        collection = self.client.db.projects

        project1 = collection.find_one({
            'url': 'http://localhost/redmine/project-1'
        })

        self.assertIsNotNone(project1)
        self.assertEqual(project1['name'], 'Project-1')
        self.assertEqual(project1['app'], 'redmine')

        project2 = collection.find_one({
            'url': 'http://localhost/gitlab/gitlab-2'
        })

        self.assertIsNotNone(project2)
        self.assertEqual(project2['name'], 'Gitlab-2')
        self.assertEqual(project2['app'], 'gitlab')

        collection = self.client.db.topics

        topic1 = collection.find_one({
            'label': 'bug',
            'project': 'http://localhost/redmine/project-1',
        })

        self.assertIsNotNone(topic1)

        topic2 = collection.find_one({
            'label': 'enhancement',
        })

        self.assertIsNotNone(topic2)

    # @unittest.expectedFailure
    def test_insert_user(self):
        collection = self.client.db.users
        documents_count = self.client.db.users.count_documents({})

        result = self.controller.insert_user({
            '_id': 10,
            'name': 'Giovanni',
            'surname': 'Masala',
            'email': None,
            'telegram': '@giovanni',
            'topics': [
                4
            ],
            'keywords': [
                'rotella',
                'java',
            ],
            'preferenza': 'telegram',
            'sostituto': 3,
        })

        self.assertIsNotNone(result)
        self.assertIsNotNone(
            collection.find_one({
                '_id': 10,
            })
        )
        self.assertEqual(
            documents_count+1,
            self.client.db.users.count_documents({}),
        )

    def test_insert_project(self):
        collection = self.client.db.projects
        documents_count = self.client.db.projects.count_documents({})

        result = self.controller.insert_project({
            "url": "http://localhost/gitlab/project-10",
            "name": "Project-10",
            "app": "gitlab",
        })

        self.assertIsNotNone(result)
        self.assertIsNotNone(
            collection.find_one({
                'name': 'Project-10',
            })
        )
        self.assertEqual(
            documents_count+1,
            self.client.db.projects.count_documents({}),
        )

    def test_insert_topic(self):
        collection = self.client.db.topics
        documents_count = self.client.db.topics.count_documents({})

        result = self.controller.insert_topic({
            "label": "wip",
            "project": "http://localhost/gitlab/project-10",
        })

        self.assertIsNotNone(result)
        self.assertIsNotNone(
            collection.find_one({
                'project': 'http://localhost/gitlab/project-10',
            })
        )
        self.assertEqual(
            documents_count+1,
            self.client.db.topics.count_documents({}),
        )

    # @unittest.skip('debugging')
    def test_delete_user(self):
        collection = self.client.db.users
        documents_count = self.client.db.users.count_documents({})

        result = self.controller.delete_one_user('@user1')

        self.assertIsNotNone(result)
        self.assertEqual(result.deleted_count, 1)
        self.assertIsNone(
            collection.find_one({
                '_id': 1,
            })
        )
        self.assertEqual(
            documents_count,
            self.client.db.users.count_documents({})+1,
        )

        # Controlla un delete fallito
        documents_count = self.client.db.users.count_documents({})
        result = self.controller.delete_one_user('aaaaa')
        self.assertEqual(
            documents_count,
            self.client.db.users.count_documents({}),
        )

    def test_delete_topic(self):
        collection = self.client.db.topics
        documents_count = self.client.db.topics.count_documents({})

        result = self.controller.delete_one_topic(
            'http://localhost/redmine/project-1',
            'bug',
        )

        self.assertIsNotNone(result)
        self.assertEqual(result.deleted_count, 1)
        self.assertIsNone(
            collection.find_one({
                'project': 'http://localhost/gitlab/project-1',
                'label': 'bug',
            })
        )
        self.assertEqual(
            documents_count,
            self.client.db.topics.count_documents({})+1,
        )

        # Controlla un delete fallito
        documents_count = self.client.db.topics.count_documents({})
        result = self.controller.delete_one_topic('aaaaa', 'aaaaa')
        self.assertEqual(
            documents_count,
            self.client.db.topics.count_documents({}),
        )

    def test_delete_project(self):
        collection = self.client.db.projects
        documents_count = self.client.db.projects.count_documents({})

        result = self.controller.delete_one_project(
            'http://localhost/redmine/project-1'
        )

        self.assertIsNotNone(result)
        self.assertEqual(result.deleted_count, 1)
        self.assertIsNone(
            collection.find_one({
                'url': 'http://localhost/redmine/project-1'
            })
        )
        self.assertEqual(
            documents_count,
            self.client.db.projects.count_documents({})+1,
        )

        # Controlla un delete fallito
        documents_count = self.client.db.projects.count_documents({})
        result = self.controller.delete_one_project('aaaaa')
        self.assertEqual(
            documents_count,
            self.client.db.projects.count_documents({}),
        )


# Funzione chiamata solo con runner.run(...)
# Scommentare le righe:
# runner = unittest.TextTestRunner()
# runner.run(suite())
# E commentare unittest.main() per customizzare
# i test da lanciare
def suite():
    suite = unittest.TestSuite()

    suite.addTest(TestDBController('test_db_instances'))

    suite.addTest(TestDBController('test_insert_user'))
    suite.addTest(TestDBController('test_insert_project'))
    suite.addTest(TestDBController('test_insert_topic'))

    suite.addTest(TestDBController('test_delete_user'))
    suite.addTest(TestDBController('test_delete_topic'))
    suite.addTest(TestDBController('test_delete_project'))

    return suite


if __name__ == '__main__':
    unittest.main()

    # runner = unittest.TextTestRunner()
    # runner.run(suite())
