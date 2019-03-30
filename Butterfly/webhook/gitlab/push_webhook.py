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
Creatore: Samuele Gardin, samuelegardin1997@gmail.com
"""

from webhook.webhook import Webhook


class GitlabPushWebhook(Webhook):
    """`GitLabPushWebhook` implementa `Webhook`.
    Parse degli eventi di Push di Gitlab.
    """

    def parse(self, whook: dict = None):
        """Parsing del file JSON. Restituisce un riferimento alla
         lista 'commits' contenente i dizionari ottenuti.
        """

        assert whook is not None

        commits = []
        # TODO: manca description, rivedere campi
        for value in whook['commits']:

            webhook = {}
            webhook['app'] = 'gitlab'
            webhook['object_kind'] = whook['object_kind']
            webhook['title'] = value['message']
            webhook['project_id'] = whook['project']['web_url']
            webhook['project_name'] = whook['project']['name']
            webhook['author'] = value['author']['name']

            webhook['added'] = []
            for content in value['added']:
                webhook['added'].append(content)
            commits.append(webhook)

            webhook['modified'] = []
            for content in value['modified']:
                webhook['modified'].append(content)
            commits.append(webhook)

            webhook['removed'] = []
            for content in value['removed']:
                webhook['removed'].append(content)
            commits.append(webhook)

        return commits
