import copy

# from mongo_db.mongointerface import MongoInterface
from mongo_db.singleton import MongoAdapter


class MongoUsers():

    def __init__(self):
        self._mongo = MongoAdapter().getInstance()

    @classmethod
    def _user_dict_no_id(cls, obj: dict):
        return {
            'name': obj['name'],
            'surname': obj['surname'],
            'telegram': obj['telegram'],
            'email': obj['email'],
            'preferenza': None,
            'topics': [],
            'keywords': [],
            'irreperibilità': obj['irreperibilità'],
            'sostituto': None,
        }

    def users(self, mongofilter={}):
        """Restituisce un `Cursor` che corrisponde al `filter` passato
        alla collezione `users`.
        Per accedere agli elementi del cursore, è possibile iterare con
        un `for .. in ..`, oppure usare il subscripting `[i]`.
        """
        return self._mongo.collection('users').find(mongofilter)

    def exists(self, mongoid: str) -> bool:
        """Restituisce `True` se l'`id` di un utente
        (che può essere Telegram o Email) è salvato nel DB.
        """
        count = self._mongo.collection('users').count_documents({
            '$or': [
                # {'_id': mongoid},
                {'telegram': mongoid},
                {'email': mongoid},
            ]
        })
        return count != 0

    def user_has_telegram(self, telegram: str) -> bool:
        """Restituisce `True` se lo user corrispondente a `id`
        ha il campo `telegram` impostato.
        """
        assert self.exists(telegram), f'User {telegram} inesistente'
        return self.exists(telegram)

    def user_has_email(self, email: str) -> bool:
        """Restituisce `True` se lo user corrispondente a `id`
        ha il campo `email` impostato.
        """
        assert self._mongo.user_exists(email), f'User {email} inesistente'
        return self.exists(email)

    def create(self, **fields):
        # Collezione di interesse
        users = self._mongo.collection('users')

        # Valori di default dei campi
        deaultfields = {
            '_id': None,
            'name': None,
            'surname': None,
            'telegram': None,
            'email': None,
            'preferenza': None,
            'irreperibilità': [],
            'sostituto': None,
            'keywords': [],
            'topics': [],
        }

        new_user = copy.copy(deaultfields)  # Copia profonda del dict default

        # Aggiorna i valori di default con quelli passati al costruttore
        for key in new_user:
            if key in fields:
                new_user[key] = fields.pop(key)

        # Inutile?
        # fields.pop('_id', True)

        assert not fields, 'Sono stati inseriti campi non validi'

        # Se telegram e email sono entrambi None
        if new_user['telegram'] is None and new_user['email'] is None:
            raise AssertionError(
                'È necessario inserire almeno un valore tra email o telegram'
            )

        # Se telegram è già presente
        # assert not self.controller.exists(new_user['telegram']), \
        #     f'Username {new_user["telegram"]} già presente'
        if (new_user['telegram'] is not None and
                users.find_one({'telegram': new_user['telegram']})):
            raise AssertionError(
                f'Username {new_user["telegram"]} già presente'
            )

        # Se email è già presente
        if (new_user['email'] is not None and
                users.find_one({'email': new_user['email']})):
            raise AssertionError(f'Email {new_user["email"]} già presente')

        # Ottiene un id valido
        if new_user['telegram'] is None:
            id = new_user['email']
        else:
            id = new_user['telegram']

        # Via libera all'aggiunta al DB
        if new_user['_id'] is None:  # Per non mettere _id = None sul DB
            partial_result = MongoUsers._user_dict_no_id(new_user)
            result = self._mongo.create(
                partial_result,
                'users'
            )

        else:
            partial_result = MongoUsers._user_dict_no_id(new_user)
            partial_result['_id'] = new_user['_id']
            result = self._mongo.create(
                partial_result,
                'users'
            )

        # NOTE: Se i dati precedenti sono validi, a questo punto sono
        # già inseriti nel DB. I dati successivi vengono inseriti
        # mano a mano che vengono considerati validi. AssertionError
        # verrà lanciata se qualcosa lo è

        # Valida e aggiunge la preferenza
        if new_user['preferenza'] is not None:
            self.update_user_preference(
                new_user[new_user['preferenza']],
                new_user['preferenza']
            )

        # Valida e aggiunge i topic
        for topic in new_user['topics']:
            self.add_user_topic_from_id(id, topic)

        # Aggiunge le kw
        self.add_keywords(id, *new_user['keywords'])

#        # Valida e aggiunge il sostituto
#        self.update_user_sostituto(id, new_user['sostituto'])

        return result

    def read(self, user: str):
        """Restituisce un oggetto Python corrispondente all'`user`
        passato come argomento.

        Raises:
        `AssertionError` -- se `user` non è presente nel DB.
        """
        assert self.exists(id), f'User {id} inesistente'

        return self.users({
            '$or': [
                {'telegram': user},
                {'email': user},
            ]
        })[0]

    def delete(self, user: str):
        """Rimuove un documento che corrisponde a
        `user`, se presente. `user` può riferirsi sia al contatto
        Telegram che email. Restituisce il risultato dell'operazione.
        """
        return self._mongo.delete(
            {
                '$or': [
                    {'telegram': user},
                    {'email': user},
                ]
            },
            'users',
        )

    def update_name(self, user: str, name: str):
        """Aggiorna il `name` dell'utente corrispondente a
        `id` (Telegram o Email).

        Raises:
        `AssertionError` -- se `id` non è presente nel DB
        """
        assert self.exists(user), f'User {user} inesistente'

        return self._mongo.collection('users').find_one_and_update(
            {'$or': [
                {'telegram': id},
                {'email': id},
            ]},
            {
                '$set': {
                    'name': name
                }
            }
        )

    def update_surname(self, user: str, surname: str):
        """Aggiorna il `surname` dell'utente corrispondente a
        `id` (Telegram o Email).

        Raises:
        `AssertionError` -- se `id` non è presente nel DB
        """
        assert self.exists(user), f'User {user} inesistente'

        return self._mongo.collection('users').find_one_and_update(
            {'$or': [
                {'telegram': id},
                {'email': id},
            ]},
            {
                '$set': {
                    'surname': surname
                }
            }
        )

    def update_telegram(self, user: str, telegram: str):
        """Aggiorna lo user ID di Telegram dell'utente corrispondente a
        `id` (Telegram o Email).

        Raises:
        `AssertionError` -- se `new_telegram` corrisponde a un
            campo `telegram` già esistente,
            se `id` non è presente nel DB oppure se tenta di
            settare a `None` mentre lo è anche `Email`.
        """
        assert self.exists(user), f'User {user} inesistente'

        assert not self.exists(telegram), \
            f'User {telegram} già presente nel sistema'

        new_telegram = 'new telegram'

        if telegram == '':
            new_telegram = None

        if new_telegram is None and not self.user_has_email(id):
            raise AssertionError('Operazione fallita. Impostare prima '
                                 'una Email')

        # self._print_user(id)
        # print(new_telegram)
        return self._mongo.collection('users').find_one_and_update(
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

    def update_email(self, user: str, email: str):
        """Aggiorna l'Email dell'utente corrispondente a
        `id` (Telegram o Email).

        Raises:
        `AssertionError` -- se `new_email` corrisponde a un
            campo `email` già esistente,
            se `id` non è presente nel DB oppure se tenta di
            settare a `None` mentre lo è anche il campo
            `telegram`.
        """
        assert self.exists(user), f'User {user} inesistente'

        assert not self.exists(email), \
            f'User {email} già presente nel sistema'

        new_email = 'new_email'

        if email == '':
            new_email = None

        if new_email is None and not self.user_has_telegram(id):
            raise AssertionError('Operazione fallita. Impostare prima '
                                 'un account Telegram')

        return self._mongo.collection('users').find_one_and_update(
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

    def update_user_preference(self, user: str, preference: str):
        """Aggiorna la preferenza (tra Telegram e Email) dell'utente
        corrispondente all'`id` (Telegram o Email).

        Raises:
        `AssertionError` -- se preference non è `telegram` o `email`
            oppure se `id` non è presente nel DB.
        """

        # Controllo validità campo preference
        assert preference.lower() in ('telegram', 'email'), \
            f'Selezione {preference} non valida: scegli tra Telegram o Email'

        # Controllo esistenza id user
        assert self.user_exists(user), f'User {id} inesistente'

        count = self._mongo.collection('users').count_documents({
            '$or': [  # Confronta id sia con telegram che con email
                {'telegram': id},
                {'email': id},
            ],
            preference: None,
        })

        # Controllo su preferenza non su un campo null
        assert count == 0, f'Il campo "{preference}" non è impostato'

        return self._mongo.collection('users').find_one_and_update(
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

    def add_keywords(self, user: str, *new_keywords):
        """Aggiunge le keywords passate come argomento all'user
        corrispondente a `id`.

        Raises:
        `AssertionError` -- se `id` non è presente nel DB.
        """
        assert self.user_exists(user), f'User {id} inesistente'
        return self._mongo.collection('users').find_one_and_update(
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

    def _get_users_by_priority(self, url: str, priority: int):
        return self.users({
            'projects': {
                '$elemMatch': {
                    'url': url,
                    'priority': priority
                },
            },
            '$currentDate': {
                '$nin': 'irreperibilità'
            }
        }, {
            '_id': 1
        })

    def get_users_available(self, url: str) -> list:
        """Dato un progetto, cerco tutti
        Gli utenti disponibili oggi
        (la lista di ritorno contiene gli ID del DB)
        """
        users = []
        for priority in range(1, 4):
            users += self._get_users_by_priority(url, priority)
        return users

    def get_users_max_priority(self, url: str) -> list:
        """Dato un progetto, ritorno la lista di
        utenti disponibili oggi di priorità maggiore
        (la lista di ritorno contiene gli ID del DB)
        """
        for priority in range(1, 4):
            max_priority = self._get_users_by_priority(url, priority)
            if max_priority:
                return max_priority
        return None

    def get_user_telegram(self, user: int):
        return self.users({
            '_id': user,
            'telegram': {'$exists': 'true', '$ne': ''}
        }, {
            'telegram': 1
        })[0]

    def get_user_email(self, user: int):
        return self.users({
            '_id': user,
            'email': {'$exists': 'true', '$ne': ''}
        }, {
            'email': 1
        })[0]
