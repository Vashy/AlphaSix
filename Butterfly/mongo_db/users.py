import copy

from mongo_db.singleton import MongoSingleton


class MongoUsers:

    def __init__(self, mongo: MongoSingleton):
        self._mongo = mongo

    @classmethod
    def _user_dict_no_id(cls, obj: dict):
        return {
            'name': obj['name'],
            'surname': obj['surname'],
            'telegram': obj['telegram'],
            'email': obj['email']
        }

    def users(self, mongofilter={}):
        """Restituisce un `Cursor` che corrisponde al `filter` passato
        alla collezione `users`.
        Per accedere agli elementi del cursore, è possibile iterare con
        un `for .. in ..`, oppure usare il subscripting `[i]`.
        """
        return self._mongo.read('users').find(mongofilter)

    def exists(self, user: str) -> bool:
        """Restituisce `True` se l'`id` di un utente
        (che può essere Telegram o Email) è salvato nel DB.
        """
        count = self._mongo.read('users').count_documents({
            '$or': [
                # {'_id': mongoid},
                {'telegram': user},
                {'email': user},
            ]
        })
        return count != 0

    def create(self, **fields):
        # Collezione di interesse
        users = self._mongo.read('users')

        # Valori di default dei campi
        defaultfields = {
            '_id': None,
            'name': None,
            'surname': None,
            'telegram': None,
            'email': None
        }

        new_user = copy.copy(defaultfields)  # Copia profonda del dict default

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
        # if new_user['telegram'] is None:
        #     identifier = new_user['email']
        # else:
        #     identifier = new_user['telegram']

        # Via libera all'aggiunta al DB
        if new_user['_id'] is None:  # Per non mettere _id = None sul DB
            partial_result = self._user_dict_no_id(new_user)
            result = self._mongo.create(
                partial_result,
                'users'
            )

        else:
            partial_result = self._user_dict_no_id(new_user)
            partial_result['_id'] = new_user['_id']
            result = self._mongo.create(
                partial_result,
                'users'
            )

        # NOTE: Se i dati precedenti sono validi, a questo punto sono
        # già inseriti nel DB. I dati successivi vengono inseriti
        # mano a mano che vengono considerati validi. AssertionError
        # verrà lanciata se qualcosa lo è

#        # Valida e aggiunge la preferenza
#        if new_user['preferenza'] is not None:
#            self.update_user_preference(
#                new_user[new_user['preferenza']],
#                new_user['preferenza']
#            )

#        # Valida e aggiunge i topic
#        for topic in new_user['topics']:
#            self.add_user_topic_from_id(id, topic)

#        # Aggiunge le kw
#        self.add_keywords(id, *new_user['keywords'])

#        # Valida e aggiunge il sostituto
#        self.update_user_sostituto(id, new_user['sostituto'])

        return result

    def read(self, user: str):
        """Restituisce un oggetto Python corrispondente all'`user`
        passato come argomento.

        Raises:
        `AssertionError` -- se `user` non è presente nel DB.
        """
        assert self.exists(user), f'User {user} inesistente'

        return self.users({
            '$or': [
                {'telegram': user},
                {'email': user},
            ]
        }).next()

    def delete_from_id(self, user: str):
        """Rimuove un documento che corrisponde a
        `user`, se presente. `user` è l'identificativo nel db
        """
        return self._mongo.delete(
            {'_id': user}, 'users'
        )

    def delete(self, user: str):
        """Rimuove un documento che corrisponde a
        `user`, che può essere `telegram` o `email`.
        """
        return self._mongo.delete({
            '$or': [
                {'telegram': user},
                {'email': user},
            ]
        }, 'users')

    def update_name(self, user: str, name: str):
        """Aggiorna il `name` dell'utente corrispondente a
        `user` (Telegram o Email).

        Raises:
        `AssertionError` -- se `user` non è presente nel DB
        """
        assert self.exists(user), f'User {user} inesistente'

        return self._mongo.read('users').find_one_and_update(
            {'$or': [
                {'telegram': user},
                {'email': user},
            ]},
            {
                '$set': {
                    'name': name
                }
            }
        )

    def update_surname(self, user: str, surname: str):
        """Aggiorna il `surname` dell'utente corrispondente a
        `user` (Telegram o Email).

        Raises:
        `AssertionError` -- se `user` non è presente nel DB
        """
        assert self.exists(user), f'User {user} inesistente'

        return self._mongo.read('users').find_one_and_update(
            {'$or': [
                {'telegram': user},
                {'email': user},
            ]},
            {
                '$set': {
                    'surname': surname
                }
            }
        )

    def _user_has_telegram(self, user: str) -> bool:
        """Restituisce `True` se lo user corrispondente a `user`
        ha il campo `telegram` impostato.
        """
        assert self.user_exists(user), f'User {user} inesistente'

        count = self.collection('users').count_documents({
            '$or': [
                {'telegram': user},
                {'email': user},
            ],
            'telegram': None,
        })
        return count != 1

    def _user_has_email(self, user: str) -> bool:
        """Restituisce `True` se lo user corrispondente a `user`
        ha il campo `email` impostato.
        """
        assert self.user_exists(user), f'User {user} inesistente'

        count = self.collection('users').count_documents({
            '$or': [
                {'telegram': user},
                {'email': user},
            ],
            'email': None,
        })
        return count != 1

    def update_telegram(self, user: str, telegram: str):
        """Aggiorna lo user ID di Telegram dell'utente corrispondente a
        `user` (Telegram o Email).

        Raises:
        `AssertionError` -- se `new_telegram` corrisponde a un
            campo `telegram` già esistente,
            se `user` non è presente nel DB oppure se tenta di
            settare a `None` mentre lo è anche `Email`.
        """
        assert self.exists(user), f'User {user} inesistente'

        assert not self.exists(telegram), \
            f'User {telegram} già presente nel sistema'

        new_telegram = telegram

        if telegram == '':
            new_telegram = None

        if new_telegram is None and not self._user_has_email(user):
            raise AssertionError('Operazione fallita. Impostare prima '
                                 'una Email')

        # self._print_user(user)
        # print(new_telegram)
        return self._mongo.read('users').find_one_and_update(
            {'$or': [
                {'telegram': user},
                {'email': user},
            ]},
            {
                '$set': {
                    'telegram': new_telegram,
                }
            }
        )

    def update_email(self, user: str, email: str):
        """Aggiorna l'Email dell'utente corrispondente a
        `user` (Telegram o Email).

        Raises:
        `AssertionError` -- se `new_email` corrisponde a un
            campo `email` già esistente,
            se `user` non è presente nel DB oppure se tenta di
            settare a `None` mentre lo è anche il campo
            `telegram`.
        """
        assert self.exists(user), f'User {user} inesistente'

        assert not self.exists(email), \
            f'User {email} già presente nel sistema'

        new_email = email

        if email == '':
            new_email = None

        if new_email is None and not self._user_has_telegram(user):
            raise AssertionError('Operazione fallita. Impostare prima '
                                 'un account Telegram')

        return self._mongo.read('users').find_one_and_update(
            {'$or': [
                {'telegram': user},
                {'email': user},
            ]},
            {
                '$set': {
                    'email': new_email,
                }
            }
        )

    def update_user_preference(self, user: str, preference: str):
        """Aggiorna la preferenza (tra Telegram e Email) dell'utente
        corrispondente all'`user` (Telegram o Email).

        Raises:
        `AssertionError` -- se preference non è `telegram` o `email`
            oppure se `user` non è presente nel DB.
        """

        # Controllo validità campo preference
        assert preference.lower() in ('telegram', 'email'), \
            f'Selezione {preference} non valida: scegli tra Telegram o Email'

        # Controllo esistenza user user
        assert self.user_exists(user), f'User {user} inesistente'

        count = self._mongo.read('users').count_documents({
            '$or': [  # Confronta user sia con telegram che con email
                {'telegram': user},
                {'email': user},
            ],
            preference: None,
        })

        # Controllo su preferenza non su un campo null
        assert count == 0, f'Il campo "{preference}" non è impostato'

        return self._mongo.read('users').find_one_and_update(
            {'$or': [  # Confronta user sia con telegram che con email
                {'telegram': user},
                {'email': user},
            ]},
            {
                '$set': {
                    'preferenza': preference
                }
            }
        )

    def add_keywords(self, user: str, project: str, *new_keywords):
        """Aggiunge le keywords passate come argomento all'user
        corrispondente a `user`.

        Raises:
        `AssertionError` -- se `user` non è presente nel DB.
        """
        assert self.user_exists(user), f'User {user} inesistente'
        return self._mongo.read('users').find_one_and_update(
            {'$or': [  # Confronta user sia con telegram che con email
                {'telegram': user},
                {'email': user},
            ]},
            {
                '$addToSet': {  # Aggiunge all'array keywords, senza duplicare
                    'keywords': {
                        '$each': [*new_keywords]  # Per ogni elemento
                    }
                }
            }
        )

    def user_keywords(self, user: str, project: str) -> list:
        """Restituisce una lista contenente le parole chiave corrispondenti
        a `project` di `user`: esso può essere sia il contatto Telegram che Email.
        """
        cursor = self.users({
            {'_id': user}
        })
        return cursor.next()['keywords']

    # TODO
    def add_labels(self, user: str, project: str, *new_labels):
        """Aggiunge le labels passate come argomento all'user
        corrispondente a `user` nel progetto `project`.

        Raises:
        `AssertionError` -- se `user` non è presente nel DB.
        """
        cursor = self._mongo.read('users').update({
            '$or': [
                {'_id': user},
                {'telegram': user},
                {'email': user},
            ],
            "projects.url": project,
        },
        {
            '$addToSet': {  # Aggiunge all'array keywords, senza duplicare
                f'{project}.$.topics': {
                    '$each': [*new_labels]  # Per ogni elemento
                }
            }
        })

    # TODO controllare se è corretta
    def user_labels(self, user: str, project: str) -> list:
        """Restituisce una lista contenente le label corrispondenti
        a `project` di `user`: esso può essere sia il contatto Telegram che Email.
        """
        cursor = self.users({
            '$or': [
                {'telegram': user},
                {'email': user},
            ]
        })
        return cursor.next()['labels']

    def _get_users_by_priority(self, project: str, priority: int):
        """Restituisce gli utenti con priorità specificata iscritti
        a `project` disponibili in data odierna.
        """
        return self.users({
            'projects': {
                '$elemMatch': {
                    'url': project,
                    'priority': priority
                },
            },
            '$currentDate': {
                '$nin': 'irreperibilita'
            }
        }, {
            '_id': 1,
        })

    def get_users_available(self, project: str) -> list:
        """Dato un progetto, cerco tutti
        Gli utenti disponibili oggi
        (la lista di ritorno contiene gli ID del DB)
        """
        users = []
        for priority in range(1, 4):  # Cicla da 1 a 3
            users += self._get_users_by_priority(project, priority)
        return users

    def get_users_max_priority(self, project: str) -> list:
        """Dato un progetto, ritorno la lista di
        utenti disponibili oggi di priorità maggiore
        (la lista di ritorno contiene gli ID del DB)
        """
        for priority in range(1, 4):
            max_priority = self._get_users_by_priority(project, priority)
            if max_priority:
                return max_priority
        return []

    def filter_max_priority(self, user_list: list, project: str) -> list:
        """Data una lista di utenti, ritorno la sottolista di
        utenti con priorità maggiore per il progetto specificato
        """
        users = []
        for priority in range(1, 4):
            max_priority = self._get_users_by_priority(project, priority)
            for user in user_list:
                if user in max_priority:
                    users.append(user)
            if users:
                return users
        return []

    def get_user_telegram_from_id(self, user: int):
        return self.users({
            '_id': user
        }).next()['telegram']

    def get_user_email_from_id(self, user: int):
        return self.users({
            '_id': user
        }).next()['email']

    def get_user_telegram(self, user: str):
        return self.users({
            '$or': [
                {'telegram': user},
                {'email': user},
            ]
        }).next()['telegram']

    def get_user_email(self, user: str):
        return self.users({
            '$or': [
                {'telegram': user},
                {'email': user},
            ]
        }).next()['email']

    def get_match_keywords(
        self,
        users: list,
        project: str,
        commit: str,
    ) -> list:
        keyword_user = []
        for user in users:
            if self.match_keyword_commit(
                self.user_keywords(user, project),
                commit
            ):
                keyword_user.append(user)

        return keyword_user

    @staticmethod
    def match_keyword_commit(
        keywords: list,
        commit_msg: str,
        case=True
    ) -> bool:
        """Restituisce `True` se `commit_msg` contiene una
        o più keyword contenute in `keywords`.
        `case` è `True` se la ricerca è case sensitive, `False`
        altrimenti.
        """
        if case is True:
            for keyword in keywords:
                if keyword in commit_msg:
                    return True
            return False

        # Case insensitive
        for keyword in keywords:
            if keyword.lower() in commit_msg.lower():
                return True
        return False

    def get_match_labels(
        self,
        users: list,
        project: str,
        labels: list,
    ) -> list:
        """Guarda se almeno una label di un user (chiamando get_user_labels) è
        presente nelle label della issue
        Per redmine c'è una sola label, per gitlab una lista
        Ritorna true se è presente almeno una label dell'utente
        nelle label della issue
        """
        label_user = []
        for user in users:
            if self.match_labels_issue(
                self.user_labels(user, project),
                labels,
            ):
                label_user.append(user)
        return label_user

    @staticmethod
    def match_labels_issue(user_labels: list, labels: list) -> bool:
        for label in user_labels:
            if label in labels:
                return True
        return False
