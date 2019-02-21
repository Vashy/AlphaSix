import json
import pprint
from pathlib import Path

import pymongo

from mongotest.db_connection import DBConnection


with DBConnection('myDB') as client:
    # print(client._db.collection_names())

    db = client.db()
    with open(Path(__file__).parent / 'db.json') as f:
        data = json.load(f)

    users_json = data['users']

    if 'users' in db.list_collection_names():
        db.drop_collection('users')

    users = db.users
    print(users.find())
    result = db.users.create_index(
        [('telegram', pymongo.ASCENDING)],
        unique=True
    )

    result = db.users.insert_many(users_json)
    # print(result)

    for user in users.find({'_id': {'$gt': 122}}):
        print(user)



    # collection = db
    # users = db.users
