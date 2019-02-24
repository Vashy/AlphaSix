import json
# import pprint
# import pymongo
from pathlib import Path

from mongo_db.db_connection import DBConnection
from mongo_db.db_controller import DBController


with DBConnection('butterfly') as client:
    # print(client._db.collection_names())

    client.drop_collections('users', 'projects', 'topics')

    controller = DBController(client)
    db = client.db
    with open(Path(__file__).parent / 'db.json') as f:
        data = json.load(f)

    users_json = data['users']
    projects_json = data['projects']
    topics_json = data['topics']

    # Popola la collezione users da db.json
    for user in users_json:
        # NON usare questo metodo per inserire utenti! Usare
        # controller.insert_user()
        result = controller.collection('users').insert_one(user)
        if result is not None:
            print(result.inserted_id)

    # Popola la collezione projects da db.json
    for project in projects_json:
        result = controller.insert_project(project)
        if result is not None:
            print(result.inserted_id)

    # Popola la collezione topics da db.json
    for topic in topics_json:
        result = controller.insert_topic(
            # topic['_id'],
            topic['label'],
            topic['project'],
        )
        if result is not None:
            print(result.inserted_id)
    # for user in users.find({}):
    #     pprint.pprint(user)
