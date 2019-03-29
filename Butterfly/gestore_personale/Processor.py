from abc import abstractmethod

from mongo_db.facade import MongoFacade


class Processor():

    def __init__(self, message: dict, mongofacade: MongoFacade):  # aggiungere riferimento DB
        self._message = message
        self._mongofacade = mongofacade

    # Metodo che chiama a ruota tutti quelli dopo per processare il messaggio
    # ex template_method
    def prepare_message(self) -> dict:
        progetto = self._check_project()  # URL progetto
        obj = self._message['object_kind']  # Issue o push ecc
        # Dict di tutti gli utenti disponibili oggi nel progetto
        utenti_disponibili = self.get_involved_users(progetto)
        # Lista di tutti gli utenti interessati e disponibili
        utenti_interessati = self._filter_users_by_topic(
            utenti_disponibili, obj
        )
        # Se non c'è nessuno, vedo la persona di priorità
        # più alta disponibile oggi per quel progetto
        if utenti_interessati == []:
            utenti_interessati = self.select_users_more_interested(
                progetto
            )
        self.__list_telegram = self.get_telegram_contacts(utenti_interessati)
        self.__list_email = self.get_email_contacts(utenti_interessati)
        final_map = {}
        final_map['telegram'] = self.__list_telegram
        final_map['email'] = self.__list_email
        return final_map

    # Controlla se c'è il progetto nel DB, se non c'è lo aggiunge
    def _check_project(self) -> str:
        urlProgetto = self._message['project_url']
        # Vediamo nel DB se il prog c'è
        exists_project = self._mongofacade.get_project_by_url(urlProgetto)
        # Se non c'è lo aggiungiamo
        if not exists_project:
            self._mongofacade.insert_project(urlProgetto)
        return urlProgetto

    # def get_users_from_project(self, project: str) -> dict:
    #     return self.__mongofacade.get_users_project(project)

    def get_involved_users(self, project: str) -> list:
        return self._mongofacade.get_users_available(project)

    # Metodo astratto che delega alle sottoclassi concrete
    # il filtraggio degli utenti in base a quelli iscritti ai topic
    @abstractmethod
    def _filter_users_by_topic(self, users: list, obj: str) -> list:
        pass

    # Lista di tutti gli utenti disponibili e più interessati
    def select_users_more_interested(self, project: str) -> list:
        return self.__mongofacade.get_users_max_priority(project)

    # Crea la lista di contatti telegram a cui inviare il messaggio
    def get_telegram_contacts(self, users: list) -> list:
        contacts = []
        for user in users:
            telegramID = self.__mongofacade.get_user_telegram(user)
            if telegramID is not None:
                contacts.append(telegramID)
        return contacts

    # Crea la lista di contatti mail a cui inviare il messaggio
    def get_email_contacts(self, users: list) -> list:
        contacts = []
        for user in users:
            emailID = self.__mongofacade.get_user_email(user)
            if emailID is not None:
                contacts.append(emailID)
        return contacts
