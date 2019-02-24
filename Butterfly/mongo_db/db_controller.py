import pymongo
import pprint
import re

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
        if (users.find_one({'telegram': user['telegram']}) and
                user['telegram'] is not None):
            print(f'Username {user["telegram"]} già presente')
            return None

        # Se email è già presente
        if (users.find_one({'email': user['email']}) and
                user['email'] is not None):
            print(f'Email {user["email"]} già presente')
            return None

        # Via libera all'aggiunta al DB
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

    def insert_topic(self, label: str, project: str):
        """Aggiunge il documento `topic` alla collezione `topics` se
        non già presente e restituisce il risultato, che può essere
        `None` in caso di chiave (`label`-`project`) duplicata.
        """
        # L'ultimo carattere dell'url di project non deve essere '/'
        if project[-1:] == '/':
            project = project[:-1]

        try:  # Tenta l'aggiunta del topic al DB
            # Ottiene l'id massimo
            max_id = (
                self.collection('topics')
                    .find()
                    .sort('_id', pymongo.DESCENDING)
                    .limit(1)[0]['_id']
            )
            # print(max_id)

            result = self.dbConnection.db['topics'].insert_one({
                '_id': max_id+1,
                'label': label,
                'project': project,
            })
            return result

        except IndexError:  # Caso in cui nessun topic è presente
            result = self.dbConnection.db['topics'].insert_one({
                '_id': 0,
                'label': label,
                'project': project,
            })
            return result

        except pymongo.errors.DuplicateKeyError as err:
            print(err)
            return None

    def delete_one_topic(
            self,
            label: str,
            project: str,
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

    def collection(
            self,
            collection_name: str
    ) -> pymongo.collection.Collection:
        """Restituisce la collezione con il nome passato come
        argomento."""
        return self.dbConnection.db[collection_name]

    def users(self, filter={}) -> pymongo.cursor.Cursor:
        """Restituisce un `Cursor` che corrisponde al `filter` passato
        alla collezione `users`.
        Per accedere agli elementi del cursore, è possibile iterare con
        un `for .. in ..`, oppure usare il subscripting `[i]`.
        """
        return self.collection('users').find(filter)

    def projects(self, filter={}) -> pymongo.cursor.Cursor:
        """Restituisce un `Cursor` che corrisponde al `filter` passato
        alla collezione `projects`.
        Per accedere agli elementi del cursore, è possibile iterare con
        un `for .. in ..`, oppure usare il subscripting `[i]`.
        """
        return self.collection('projects').find(filter)

    def topics(self, filter={}) -> pymongo.cursor.Cursor:
        """Restituisce un `Cursor` che corrisponde al `filter` passato
        alla collezione `topics`.
        Per accedere agli elementi del cursore, è possibile iterare con
        un `for .. in ..`, oppure usare il subscripting `[i]`.
        """
        return self.collection('topics').find(filter)

    def user_keywords(self, id: str) -> list:
        """Restituisce una lista contenente le parole chiave corrispondenti
        all'`id`: esso può essere sia il contatto Telegram che Email.
        """
        cursor = self.users({
            '$or': [
                {'telegram': id},
                {'email': id},
            ]
        })
        return cursor[0]['keywords']

    def user_topics(self, id: str) -> list:
        """Restituisce una `Cursor` contenente i topic corrispondenti
        all'`id` del'utente: `id` può essere sia il contatto
        Telegram che Email.
        """
        assert self.user_exists(id), f'User {id} inesistente'

        cursor = self.users({
            '$or': [
                {'telegram': id},
                {'email': id},
            ]
        })
        topic_ids = cursor[0]['topics']

        # Match di tutti i topic che hanno un _id contenuto in topic_ids
        return self.topics({
            '_id': {
                '$in': topic_ids,
            }
        })

    def add_user_topic(self, id: str, label: str, project: str) -> list:
        assert self.user_exists(id), f'User {id} inesistente'
        assert self.project_exists(project), 'Progetto sconosciuto'
        assert self.topic_exists(label, project), 'Topic inesistente'

        topic_id = self.topics({'label': label, 'project': project})[0]['_id']
        return self.collection('users').find_one_and_update(
            {'$or': [  # Confronta id sia con telegram che con email
                {'telegram': id},
                {'email': id},
            ]},
            {
                '$addToSet': {  # Aggiunge all'array topics, senza duplicare
                    'topics': topic_id,
                }
            }
        )

    def add_keywords(self, id: str, *new_keywords):
        assert self.user_exists(id), f'User {id} inesistente'
        return self.collection('users').find_one_and_update(
            {'$or': [  # Confronta id sia con telegram che con email
                {'telegram': id},
                {'email': id},
            ]},
            {
                '$addToSet': {  # Aggiunge all'array keywords, senza duplicare
                    'keywords': {
                        '$each': [*new_keywords]  # Per ogni elemento
                    }
                }
            }
        )

    # -------------------
    # | Esistenza campi |
    # -------------------

    def project_exists(self, url: str) -> bool:
        count = self.collection('projects').count_documents({
            'url': url,
        })
        if count == 0:
            return False
        return True

    def topic_exists(self, label: str, project: str) -> bool:
        count = self.collection('topics').count_documents({
            'label': label,
            'project': project,
        })
        if count == 0:
            return False
        return True

    def user_exists(self, id: str) -> bool:
        count = self.collection('users').count_documents({
            '$or': [
                {'telegram': id},
                {'email': id},
            ]
        })
        if count == 0:
            return False
        return True

    # --------------------
    # | Update user data |
    # --------------------

    def update_user_preferece(self, id: str, preference: str):

        # Controllo validità campo preference
        assert preference.lower() in ('telegram', 'email'), \
            f'Selezione {preference} non valida: scegli tra Telegram o Email'

        # Controllo esistenza id user
        assert self.user_exists(id), f'User {id} inesistente'

        count = self.collection('users').count_documents({
            '$or': [  # Confronta id sia con telegram che con email
                {'telegram': id},
                {'email': id},
            ],
            preference: None,
        })

        # Controllo su preferenza non su un campo null
        assert count == 0, f'Il campo "{preference}" non è impostato'

        return self.collection('users').find_one_and_update(
            {'$or': [  # Confronta id sia con telegram che con email
                {'telegram': id},
                {'email': id},
            ]},
            {
                '$set': {
                    'preferenza': preference
                }
            }
        )

    def update_user_telegram(self, id: str, new_telegram: str):
        assert self.user_exists(id), f'User {id} inesistente'

        assert not self.user_exists(new_telegram), \
            f'User {new_telegram} già presente nel sistema'

        if new_telegram == '':
            new_telegram = None

        if new_telegram is None and not self.user_has_email(id):
            raise AssertionError('Operazione fallita. Impostare prima ' 
                                 'una Email')

        # self._print_user(id)
        # print(new_telegram)
        return self.collection('users').find_one_and_update(
            {'$or': [
                {'telegram': id},
                {'email': id},
            ]},
            {
                '$set': {
                    'telegram': new_telegram,
                }
            }
        )

    def update_user_email(self, id: str, new_email: str):
        assert self.user_exists(id), f'User {id} inesistente'

        assert not self.user_exists(new_email), \
            f'User {new_email} già presente nel sistema'

        if new_email == '':
            new_email = None

        if new_email is None and not self.user_has_telegram(id):
            raise AssertionError('Operazione fallita. Impostare prima ' 
                                 'un account Telegram')

        return self.collection('users').find_one_and_update(
            {'$or': [
                {'telegram': id},
                {'email': id},
            ]},
            {
                '$set': {
                    'email': new_email,
                }
            }
        )

    def update_user_name(self, id: str, new_name: str):
        assert self.user_exists(id), f'User {id} inesistente'

        return self.collection('users').find_one_and_update(
            {'$or': [
                {'telegram': id},
                {'email': id},
            ]},
            {
                '$set': {
                    'name': new_name
                }
            }
        )

    def update_user_surname(self, id: str, new_surname: str):
        assert self.user_exists(id), f'User {id} inesistente'

        return self.collection('users').find_one_and_update(
            {'$or': [
                {'telegram': id},
                {'email': id},
            ]},
            {
                '$set': {
                    'surname': new_surname
                }
            }
        )

    def user_has_telegram(self, id: str) -> bool:
        assert self.user_exists(id), f'User {id} inesistente'

        count = self.collection('users').count_documents({
            '$or': [
                {'telegram': id},
                {'email': id},
            ],
            'telegram': None,
        })
        if count == 1:
            return False
        return True

    def user_has_email(self, id: str) -> bool:
        assert self.user_exists(id), f'User {id} inesistente'

        count = self.collection('users').count_documents({
            '$or': [
                {'telegram': id},
                {'email': id},
            ],
            'email': None,
        })
        if count == 1:
            return False
        return True

    def _print_user(self, id):
        pprint.pprint(self.users({
            '$or': [
                {'telegram': id},
                {'email': id},
            ]
        })[0])

    @property
    def dbConnection(self):
        return self._dbConnection

    def user(self, id):
        assert self.user_exists(id), f'User {id} inesistente'

        return self.users({
            '$or': [
                {'telegram': id},
                {'email': id},
            ]
        })[0]
