import copy

from mongo_db.mongointerface import MongoInterface
from mongo_db.mongosingleton import MongoAdapter


class MongoUsers(MongoInterface):

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

    def users(self, filter={}):
        """Restituisce un `Cursor` che corrisponde al `filter` passato
        alla collezione `users`.
        Per accedere agli elementi del cursore, è possibile iterare con
        un `for .. in ..`, oppure usare il subscripting `[i]`.
        """
        return self._mongo.collection('users').find(filter)

    def exists(self, id: str) -> bool:
        """Restituisce `True` se l'`id` di un utente
        (che può essere Telegram o Email) è salvato nel DB.
        """
        count = self._mongo.collection('users').count_documents({
            '$or': [
                # {'_id': id},
                {'telegram': id},
                {'email': id},
            ]
        })
        if count == 0:
            return False
        return True

    def create(self, **fields):
        # Collezione di interesse
        users = self._mongo.collection('users')

        # Valori di default dei campi
        FIELDS = {
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

        new_user = copy.copy(FIELDS)  # Copia profonda del dict FIELDS

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
        # assert not self.controller.user_exists(new_user['telegram']), \
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
            result = self._insert_document(
                partial_result,
                'users',
            )

        else:
            partial_result = MongoUsers._user_dict_no_id(new_user)
            partial_result['_id'] = new_user['_id']
            result = self._insert_document(
                partial_result,
                'users',
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

        # Valida e aggiunge il sostituto
        self.update_user_sostituto(id, new_user['sostituto'])

        return result

    def read(self, id):
        """Restituisce un oggetto Python corrispondente all'`id`
        passato come argomento.

        Raises:
        `AssertionError` -- se `id` non è presente nel DB.
        """
        assert self.user_exists(id), f'User {id} inesistente'

        return self.users({
            '$or': [
                {'telegram': id},
                {'email': id},
            ]
        })[0]

    def delete(self, user: str):
        """Rimuove un documento che corrisponde a
        `user`, se presente. `user` può riferirsi sia al contatto
        Telegram che email. Restituisce il risultato dell'operazione.
        """
        return self._delete_one_document(
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
        assert self.user_exists(id), f'User {id} inesistente'

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
        assert self.user_exists(id), f'User {id} inesistente'

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
        assert self.user_exists(id), f'User {id} inesistente'

        assert not self.user_exists(telegram), \
            f'User {telegram} già presente nel sistema'

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
        assert self.user_exists(id), f'User {id} inesistente'

        assert not self.user_exists(email), \
            f'User {email} già presente nel sistema'

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
