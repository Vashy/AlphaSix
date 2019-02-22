import pymongo

from mongo_db.db_connection import DBConnection


# Non credo che controller sia il termine adatto
class DBController(object):
    def __init__(self, db: DBConnection):
        self._dbConnection = db
        # Rende unique l'url dei progetti
        db.db['projects'].create_index(
            [('url', pymongo.ASCENDING)],
            unique=True,
        )
        # Rende unica la coppia label-project di topics
        db.db['topics'].create_index(
            [('label', pymongo.ASCENDING),
                ('project', pymongo.ASCENDING)],
            unique=True,
        )

    def insert_document(
            self,
            document: dict,
            collection: str,
    ) -> pymongo.collection.InsertOneResult:
        """Aggiunge il documento `document` alla collezione
        `collection`
        """
        result = self.dbConnection.db[collection].insert_one(document)
        return result

    def insert_user(self, user: dict):
        """Aggiunge il documento `user` alla collezione `users`
        """
        users = self.dbConnection.db['users']

        # Se telegram e email sono entrambi None
        if user['telegram'] is None and user['email'] is None:
            print(f'User {user["name"]} {user["surname"]} '
                  'non ha ne contatto Telegram ne email')

        # Se telegram è già presente
        elif (users.find_one({'telegram': user['telegram']}) and
                user['telegram'] is not None):
            print(f'Username {user["telegram"]} già presente')

        # Se email è già presente
        elif (users.find_one({'email': user['email']}) and
                user['email'] is not None):
            print(f'Email {user["email"]} già presente')

        # Via libera all'aggiunta al DB
        else:
            result = self.insert_document(user, 'users')
            print(result.inserted_id)

    def insert_topic(self, topic):
        """Aggiunge il documento `topic` alla collezione `topics`
        """
        try:  # Tenta l'aggiunta del topic al DB
            result = self.dbConnection.db['topics'].insert_one(topic)
            # Stampa l'id se l'aggiunta avviene con successo
            print(result.inserted_id)
        except pymongo.errors.DuplicateKeyError as err:
            print(err)

    def insert_project(self, project: dict):
        """Aggiunge il documento `project` alla collezione `projects`
        """
        try:  # Tenta l'aggiunta del progetto
            result = self.dbConnection.db['projects'].insert_one(project)
            # Stampa l'id se l'aggiunta avviene con successo
            print(result.inserted_id)
        # url già presente, segnala l'errore
        # e prosegue con il prossimo documento
        except pymongo.errors.DuplicateKeyError as err:
            print(err)

    @property
    def dbConnection(self):
        return self._dbConnection
