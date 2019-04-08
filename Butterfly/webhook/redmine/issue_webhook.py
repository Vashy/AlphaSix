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

from webhook.webhook import Webhook


class RedmineIssueWebhook(Webhook):
    """GitLab Issue event Webhook"""

    def parse(self, whook: dict):
        """Parsing del file JSON associato al webhook."""

        assert whook is not None

        webhook = {}
        webhook['app'] = 'redmine'
        webhook['object_kind'] = 'issue'
        webhook['title'] = whook['payload']['issue']['subject']
        webhook['description'] = whook['payload']['issue']['description']
        webhook['project_id'] = whook['payload']['issue']['project']['id']
        webhook['project_name'] = whook['payload']['issue']['project']['name']
        webhook['action'] = whook["payload"]["action"]
        webhook['author'] = whook['payload']['issue']['author']['firstname']
        # webhook['assignees'] = (
        #     whook['payload']['issue']['assignee']['firstname']
        # )
        webhook['labels'] = whook['payload']['issue']['tracker']['name']

        webhook['update'] = {}

        if 'journal' in whook['payload']:
            webhook['update']['comment'] = whook['payload']['journal']['notes']
            webhook['update']['author'] = (
                whook['payload']['journal']['author']['firstname']
            )

            for value in whook['payload']['journal']['details']:
                attribute = value['prop_key'].replace('_id', '')
                webhook['update'][attribute] = (
                    whook['payload']['issue'][attribute]['name']
                )

        return webhook
