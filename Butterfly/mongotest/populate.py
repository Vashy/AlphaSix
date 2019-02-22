import json
import pprint
from pathlib import Path

import pymongo

from mongotest.db_connection import DBConnection


with DBConnection('myDB') as client:
    print(client._db.collection_names())

    db = client.db
    with open(Path(__file__).parent / 'db.json') as f:
        data = json.load(f)

    client.drop_collections('users', 'projects', 'topics')

    users_json = data['users']
    users = db.users  # Prepara la collezione users

    projects_json = data['projects']
    projects = db.projects  # Prepara la collezione projects

    topics_json = data['topics']
    topics = db.topics  # Prepara la collezione topics

    # Popola la collezione users da db.json
    for user in users_json:
        if user['telegram'] is None and user['email'] is None:
            print(f'User {timoty}')
        # Se telegram è già presente
        if users.find_one({'telegram': user['telegram']}):
            print(f'Username {user["telegram"]} già presente')

        # Se email è già presente
        elif users.find_one({'email': user['email']}):
            print(f'Email {user["email"]} già presente')

        # Via libera all'aggiunta al DB
        else:
            result = users.insert_one(user)
            print(result.inserted_id)

    # Rende unique l'url dei progetti
    projects.create_index(
        [('url', pymongo.ASCENDING)],
        unique=True,
    )

    # Popola la collezione projects da db.json
    for project in projects_json:
        try:  # Tenta l'aggiunta del progetto
            result = projects.insert_one(project)
            # Stampa l'id se l'aggiunta avviene con successo
            print(result.inserted_id)
        # url già presente, segnala l'errore
        # e prosegue con il prossimo documento
        except pymongo.errors.DuplicateKeyError as err:
            print(err)

    # Rende unica la coppia label-project di topics
    topics.create_index(
        [('label', pymongo.ASCENDING),
            ('project', pymongo.ASCENDING)],
        unique=True,
    )

    # Popola la collezione topics da db.json
    for topic in topics_json:
        try:  # Tenta l'aggiunta del topic al DB
            result = topics.insert_one(topic)
            # Stampa l'id se l'aggiunta avviene con successo
            print(result.inserted_id)
        except pymongo.errors.DuplicateKeyError as err:
            print(err)

    # for user in users.find({}):
    #     pprint.pprint(user)
