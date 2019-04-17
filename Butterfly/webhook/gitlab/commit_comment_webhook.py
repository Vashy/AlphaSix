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


class GitlabCommitCommentWebhook(Webhook):
    """`GitLabCommitCommentWebhook` implementa `Webhook`.
    Parse degli eventi di commento di un Commit di Gitlab.
    """

    def parse(self, whook: dict = None):
        """Parsing del file JSON. Restituisce un riferimento al dizionario
        ottenuto.
        """

        assert whook is not None

        webhook = {}
        webhook['app'] = 'gitlab'
        webhook['object_kind'] = 'commit-note'  # whook['object_kind']
        webhook['title'] = whook['commit']['message']
        webhook['project_id'] = whook['project']['web_url']
        webhook['project_name'] = whook['project']['name']
        webhook['author'] = whook['user']['name']
        webhook['description'] = whook['object_attributes']['note']
        webhook['action'] = 'comment'

        return webhook
