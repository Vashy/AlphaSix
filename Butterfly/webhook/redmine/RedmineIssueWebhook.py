"""
File: RedmineIssueWebhook.py
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
Creatore: Laura Cameran, lauracameran@gmail.com
Autori:
    Samuele Gardin, samuelegardin@gmail.com
"""

import json
from pathlib import Path  # Gestione del File System in modo intelligente
from webhook.webhook import Webhook

# FIXME: Tim ~ Secondo me da rivedere, per renderlo stateless.
# e.g. passando come parametri alla funzione parse().
# Di conseguenza, rivedere i metodi astratti dell'interfaccia Webhook


class RedmineIssueWebhook(Webhook):
    """GitLab Issue event Webhook"""

    def __init__(self, whook: dict):
        self._webhook = None
        self._json_webhook = whook

    def parse(self):
        """Parsing del file JSON associato al webhook."""

        webhook = {}

        webhook["app"] = 'redmine'
        webhook["title"] = self._json_webhook["payload"]["issue"]["subject"]
        webhook["description"] = (
            self._json_webhook["payload"]["issue"]["description"]
        )
        webhook["project_id"] = (
            self._json_webhook["payload"]["issue"]["project"]["id"]
        )
        webhook["project_name"] = (
            self._json_webhook["payload"]["issue"]["project"]["name"]
        )
        webhook["action"] = self._json_webhook["payload"]["action"]
        webhook["author"] = (
            self._json_webhook["payload"]["issue"]["author"]["firstname"]
        )
        webhook["assignees"] = self._json_webhook["payload"]["issue"]["assignee"]

        self._webhook = webhook

        # webhook["issue_id"] = self._json_webhook["payload"]["issue"]["id"]    NON USATA
        # webhook["status"] = self._json_webhook["payload"]["issue"]["status"]["name"]  NON USATA
        # webhook["tracker"] = self._json_webhook["payload"]["issue"]["tracker"]["name"]    NON USATA
        # webhook["priority"] = self._json_webhook["payload"]["issue"]["priority"]["name"]  NON USATA
        # webhook["assignees"] = []
        # for value in self._json_webhook['payload']['issue']['assignee']:
        #     webhook["assignees"].append(value["firstname"])

        # TODO: Da continuare, con tutti i campi di interesse
        #  definiti nel .json

    @property
    def webhook(self):
        """Restituisce l'oggetto Python associato al Webhook, solo
        con i campi di interesse.
        """
        return self._webhook
