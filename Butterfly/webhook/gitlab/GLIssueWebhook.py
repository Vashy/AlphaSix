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

    def __init__(self, path: str):
        self._webhook = None

        # Controlla che il percorso sia effettivamente valido
        if not Path(path).is_file():
            raise FileNotFoundError(f'{path} non è un file')

        # Deserialize fp to a Python object.
        # With chiude in automatico alla fine
        with open(path) as f:
            self._json_file = json.load(f)

    def parse(self):
        """Parsing del file JSON associato al webhook."""

        webhook = {}
        webhook["type"] = 'Gitlab'
        webhook["object_kind"] = self._json_file["object_kind"]
        webhook["title"] = self._json_file["object_attributes"]["title"]
        webhook["project"] = {}
        webhook["project_id"] = self._json_file["project"]["id"]
        webhook["project_name"] = self._json_file["project"]["name"]
        webhook["author"] = self._json_file["user"]["name"]

        webhook["assignees"] = []
        for value in self._json_file["assignees"]:
            webhook["assignees"].append(value)

        webhook["action"] = self._json_file["object_attributes"]["action"]
        webhook["description"] = (
            self._json_file["object_attributes"]["description"]
        )

        webhook["labels"] = []
        for value in self._json_file["labels"]:
            webhook["labels"].append(value["title"])

        webhook["changes"] = {}
        webhook["changes"]["labels"] = {}
        webhook["changes"]["labels"]["previous"] = (
            self._json_file["changes"]["labels"]["previous"]
        )
        webhook["changes"]["labels"]["current"] = (
            self._json_file["changes"]["labels"]["current"]
        )
        self._webhook = webhook

        # TODO: Da continuare, con tutti i campi di interesse
        #  definiti in webhook.json

    @property
    def webhook(self):
        """Restituisce l'oggetto Python associato al Webhook, solo
        con i campi di interesse.
        """
        return self._webhook
