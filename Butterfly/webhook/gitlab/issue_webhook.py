"""
File: GitlabIssueWebhook.py
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

Versione: 0.2.0
Creatore: Timoty Granziero, timoty.granziero@gmail.com
Autori:
    Laura Cameran, lauracameran@gmail.com
"""

import json
from pathlib import Path
from webhook.webhook import Webhook

# FIXME: Tim ~ Secondo me da rivedere, per renderlo stateless.
# e.g. passando come parametri alla funzione parse().
# Di conseguenza, rivedere i metodi astratti dell'interfaccia Webhook


class GitlabIssueWebhook(Webhook):
    """GitLab Issue event Webhook"""

    def __init__(self, whook: object):
        self._webhook = None
        self._json_webhook = whook

    def parse(self):
        """Parsing del file JSON associato al webhook."""

        webhook = {}
        webhook["app"] = 'gitlab'
        webhook["object_kind"] = self._json_webhook["object_kind"]
        webhook["title"] = self._json_webhook["object_attributes"]["title"]
        webhook["project"] = {}
        webhook["project_id"] = self._json_webhook["project"]["id"]
        webhook["project_name"] = self._json_webhook["project"]["name"]
        webhook["author"] = self._json_webhook["user"]["name"]

        webhook["assignees"] = []
        for value in self._json_webhook["assignees"]:
            webhook["assignees"].append(value)

        webhook["action"] = self._json_webhook["object_attributes"]["action"]
        webhook["description"] = (
            self._json_webhook["object_attributes"]["description"]
        )

        webhook["labels"] = []
        for value in self._json_webhook["labels"]:
            webhook["labels"].append(value["title"])

        webhook["changes"] = {}
        webhook["changes"]["labels"] = {}
        webhook["changes"]["labels"]["previous"] = (
            self._json_webhook["changes"]["labels"]["previous"]
        )
        webhook["changes"]["labels"]["current"] = (
            self._json_webhook["changes"]["labels"]["current"]
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
