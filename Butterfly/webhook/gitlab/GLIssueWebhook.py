"""
File: GLIssueWebhook.py
Data creazione: 2019-02-15

<descrizione>

Licenza: Apache 2.0

Copyright 2019 AlphaSix

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Versione: 0.1.0
Creatore: Timoty Granziero, timoty.granziero@gmail.com
Autori:
    <nome cognome, email>
    <nome cognome: email>
    ....
"""

import json
from pathlib import Path
from webhook.webhook import Webhook

# FIXME: Tim ~ Secondo me da rivedere, per renderlo stateless.
# e.g. passando come parametri alla funzione parse().
# Di conseguenza, rivedere i metodi astratti dell'interfaccia Webhook
class GLIssueWebhook(Webhook):
    """GitLab Issue event Webhook"""

    def __init__(self, jsonfile=None):
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
        webhook["project_id"] = self.json_file["project"]["id"]
        webhook["project_name"] = self.json_file["project"]["name"]
        webhook["author"] = self.json_file["user"]["name"]

        webhook["assignees"] = []
        for value in self.json_file["assignees"]:
            webhook["assignees"].append(value["username"])

        webhook["action"] = self.json_file["object_attributes"]["action"]
        webhook["description"] = self.json_file["object_attributes"]["description"]

        webhook["labels"] = []
        for value in self.json_file["labels"]:
            #print('value: ' + value)
            print(type(value))
            webhook["labels"].append(value["title"])

        webhook["changes"] = {}
        webhook["changes"]["labels"] = {}
        webhook["changes"]["labels"]["previous"] = (
            self.json_file["changes"]["labels"]["previous"]
        )
        webhook["changes"]["labels"]["current"] = (
            self.json_file["changes"]["labels"]["current"]
        )
        self._webhook = webhook

        # TODO: Da continuare, con tutti i campi di interesse
        #  definiti in webhook.json 

    def webhook(self):
        """Restituisce l'oggetto Python associato al Webhook, solo
        con i campi di interesse.
        """
        return self._webhook
