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

from webhook.webhook import Webhook

# FIXME: Tim ~ Secondo me da rivedere, per renderlo stateless.
# e.g. passando come parametri alla funzione parse().
# Di conseguenza, rivedere i metodi astratti dell'interfaccia Webhook


class GitlabIssueWebhook(Webhook):
    """GitLab Issue event Webhook"""

    def __init__(self, whook: dict = None):
        self._webhook = whook

    def parse(self, whook: dict = None):
        """Parsing del file JSON associato al webhook."""

        if self._webhook is not None:
            return self._webhook

        assert whook is not None

        self._webhook = {}
        self._webhook["app"] = 'gitlab'
        self._webhook["object_kind"] = whook["object_kind"]
        self._webhook["title"] = whook["object_attributes"]["title"]
        self._webhook["project"] = {}
        self._webhook["project_id"] = whook["project"]["id"]
        self._webhook["project_name"] = whook["project"]["name"]
        self._webhook["author"] = whook["user"]["name"]

        self._webhook["assignees"] = []
        for value in whook["assignees"]:
            self._webhook["assignees"].append(value)

        self._webhook["action"] = whook["object_attributes"]["action"]
        self._webhook["description"] = (
            whook["object_attributes"]["description"]
        )

        self._webhook["labels"] = []
        for value in whook["labels"]:
            self._webhook["labels"].append(value["title"])

        self._webhook["changes"] = {}
        self._webhook["changes"]["labels"] = {}
        self._webhook["changes"]["labels"]["previous"] = (
            whook["changes"]["labels"]["previous"]
        )
        self._webhook["changes"]["labels"]["current"] = (
            whook["changes"]["labels"]["current"]
        )

        return self._webhook

        # TODO: Da continuare, con tutti i campi di interesse
        #  definiti in webhook.json

    # @property
    # def webhook(self):
    #     """Restituisce l'oggetto Python associato al Webhook, solo
    #     con i campi di interesse.
    #     """
    #     return self._webhook
