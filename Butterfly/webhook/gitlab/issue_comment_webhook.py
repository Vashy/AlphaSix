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
import requests

from webhook.webhook import Webhook


class GitlabIssueCommentWebhook(Webhook):
    """`GitLabIssueCommentWebhook` implementa `Webhook`.
    Parse degli eventi di commento di una Issue di Gitlab.
    """

    def parse(self, whook: dict = None):
        """Parsing del file JSON. Restituisce un riferimento al dizionario
        ottenuto.
        """

        assert whook is not None
        # p_id = whook['project']['id']
        # result = requests.get(
        #     f'http://localhost:80/api/v4/projects/{p_id}/labels',
        #     headers={'PRIVATE-TOKEN': 'ChqrHpxfCsFsCY1N28Wx'}
        # )

        webhook = {}
        webhook['app'] = 'gitlab'
        webhook['object_kind'] = 'issue-note'
        webhook['title'] = whook['issue']['title']
        webhook['project_id'] = whook['project']['web_url']
        webhook['project_name'] = whook['project']['name']
        webhook['author'] = whook['user']['name']
        webhook['comment'] = whook['object_attributes']['description']

        labels = self.project_labels(
            'http://localhost:80',
            whook['project']['id'],
            'ChqrHpxfCsFsCY1N28Wx',
        )
        webhook['labels'] = labels
        return webhook

    def project_labels(self, home_url: str, project_id: str, token: str):
        result = requests.get(
            f'{home_url}/api/v4/projects/{project_id}/labels',
            headers={'PRIVATE-TOKEN': token}
        )
        labels = []
        if result.ok:
            for label in result.json():
                labels.append(label['name'])
        return labels
