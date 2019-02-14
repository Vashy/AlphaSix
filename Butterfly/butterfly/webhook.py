import json
from abc import ABC, abstractmethod
from pathlib import Path


class Webhook(ABC):
    """Interfaccia Webhook"""

    @property
    @abstractmethod
    def json_file(self):
        """Restituisce il file JSON associato al webhook."""
        pass

    @json_file.setter
    @abstractmethod
    def json_file(self, jsonfile):
        """Setter della property json_file"""
        pass

    @abstractmethod
    def parse(self):
        """Parsing del file JSON associato al webhook."""
        pass

    @abstractmethod
    def webhook(self):
        """Restituisce l'oggetto Python associato al JSON del webhook.
        Precondizione: `parse()` è stato chiamato almeno una volta,
            altrimenti restituirà None.
        """
        pass


class GLIssueWebhook(Webhook):
    """GitLab Issue event Webhook"""

    def __init__(self, jsonfile = None):
        self.json_file = jsonfile
        self._webhook = None

    @property
    def json_file(self):
        """Restituisce il file JSON associato al webhook."""
        return self._json_file

    @json_file.setter
    def json_file(self, jsonfile):
        """Setter della property json_file"""

        # Controlla se jsonfile è istanza di Path, str o None

        if isinstance(jsonfile, Path):
            path = jsonfile
            if not path.is_file(): # Se non è un file
                raise FileNotFoundError()

            with open(path) as f:
                self._json_file = json.load(f)

        elif isinstance(jsonfile, str):
            path = Path(jsonfile)
            if not path.is_file(): # Se non è un file
                raise FileNotFoundError()

            with open(path) as f:
                self._json_file = json.load(f)

        elif jsonfile is not None:
            raise TypeError()

        else:
            self._json_file = jsonfile


    def parse(self):
        """Parsing del file JSON associato al webhook."""
        if self.json_file is None:
            raise FileNotFoundError()

        webhook = {}
        webhook["object_kind"] = self.json_file["object_kind"]
        webhook["title"] = self.json_file["object_attributes"]["title"]
        webhook["project"] = {}
        webhook["project"]["id"] = self.json_file["project"]["id"]
        webhook["project"]["name"] = self.json_file["project"]["name"]

        webhook["assignees"] = []
        for value in self.json_file["assignees"]:
            webhook["assignees"].append(value["username"])

        webhook["action"] = self.json_file["object_attributes"]["action"]
        webhook["description"] = self.json_file["object_attributes"]["description"]

        webhook["labels"] = []
        for value in self.json_file["labels"]:
            webhook["labels"].append(value["title"])

        webhook["changes"] = {}
        webhook["changes"]["labels"] = {}
        webhook["changes"]["labels"]["previous"] = \
            self.json_file["changes"]["labels"]["previous"]
        webhook["changes"]["labels"]["current"] = \
            self.json_file["changes"]["labels"]["current"]
        self._webhook = webhook

    def webhook(self):
        """Restituisce l'oggetto Python associato al Webhook, solo
        con i campi di interesse.
        """
        return self._webhook
