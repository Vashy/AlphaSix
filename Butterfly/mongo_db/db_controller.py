import pymongo

from mongo_db.db_connection import DBConnection


# Non credo che controller sia il termine adatto
class DBController(object):
    def __init__(self, db: DBConnection, indexes=True):
        self._dbConnection = db
        if indexes:
            self.initialize_indexes()

    def initialize_indexes(self):
        # Rende unique l'url dei progetti
        self.dbConnection.db['projects'].create_index(
            [('url', pymongo.ASCENDING)],
            unique=True,
        )
        # Rende unica la coppia label-project di topics
        self.dbConnection.db['topics'].create_index(
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
        `collection`, se non è già presente.
        """
        result = self.dbConnection.db[collection].insert_one(document)
        return result

    def delete_one_document(
            self,
            filter: dict,
            collection: str,
    ) -> pymongo.collection.DeleteResult:
        """Rimuove un documento che corrisponde al
        `filter`, se presente, e restituisce il risultato.
        """
        result = self.dbConnection.db[collection].delete_one(filter)
        return result

    def insert_user(self, user: dict) -> pymongo.collection.InsertOneResult:
        """Aggiunge il documento `user` alla collezione `users` se non
        già presente (il controllo è sui contatti Telegram e email).
        Inoltre, i campi `telegram` e `email` non possono essere
        entrambi None.
        Restituisce il risultato, che può essere
        `None` in caso di chiave duplicata.
        """
        users = self.dbConnection.db['users']

        # Se telegram e email sono entrambi None
        if user['telegram'] is None and user['email'] is None:
            print(f'User {user["name"]} {user["surname"]} '
                  'non ha ne contatto Telegram ne email')
            return None

        # Se telegram è già presente
        elif (users.find_one({'telegram': user['telegram']}) and
                user['telegram'] is not None):
            print(f'Username {user["telegram"]} già presente')
            return None

        # Se email è già presente
        elif (users.find_one({'email': user['email']}) and
                user['email'] is not None):
            print(f'Email {user["email"]} già presente')
            return None

        # Via libera all'aggiunta al DB
        else:
            # print(result.inserted_id)
            return self.insert_document(user, 'users')

    def delete_one_user(self, user: str) -> pymongo.collection.DeleteResult:
        """Rimuove un documento che corrisponde a
        `user`, se presente. `user` può riferirsi sia al contatto
        Telegram che email. Restituisce il risultato dell'operazione.
        """
        return self.delete_one_document(
            {
                '$or': [
                    {'telegram': user},
                    {'email': user},
                ]
            },
            'users',
        )

    def insert_topic(self, topic):
        """Aggiunge il documento `topic` alla collezione `topics` se
        non già presente e restituisce il risultato, che può essere
        `None` in caso di chiave (`label`-`project`) duplicata.
        """
        # L'ultimo carattere dell'url di project non deve essere '/'
        if topic['project'][-1:] == '/':
            topic['project'] = topic['project'][:-1]
        try:  # Tenta l'aggiunta del topic al DB
            result = self.dbConnection.db['topics'].insert_one(topic)
            return result
        except pymongo.errors.DuplicateKeyError as err:
            print(err)
            return None

    def delete_one_topic(
            self,
            project: str,
            label: str,
    ) -> pymongo.collection.DeleteResult:
        """Rimuove un documento che corrisponda alla coppia `label`-`project`,
        se presente, e restituisce il risultato.
        """
        return self.delete_one_document({
                'label': label,
                'project': project,
            },
            'topics',
        )

    def insert_project(self, project: dict):
        """Aggiunge il documento `project` alla collezione `projects`,
        se non già presente, e restituisce il risultato, che può essere
        `None` in caso di chiave duplicata.
        """
        # L'ultimo carattere non deve essere '/'
        if project['url'][-1:] == '/':
            project['url'] = project['url'][:-1]
        try:  # Tenta l'aggiunta del progetto
            result = self.dbConnection.db['projects'].insert_one(project)
            return result
        # url già presente, segnala l'errore
        # e prosegue con il prossimo documento
        except pymongo.errors.DuplicateKeyError as err:
            print(err)
            return None

    def delete_one_project(
            self,
            url: str,
    ) -> pymongo.collection.DeleteResult:
        """Rimuove un documento che corrisponda a `url`,
        se presente, e restituisce il risultato.
        """
        return self.delete_one_document({
                'url': url,
            },
            'projects'
        )

    @property
    def dbConnection(self):
        return self._dbConnection
