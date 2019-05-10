"""
File: push_webhook.py
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

    def parse(self, whook: dict):
        """Parsing del file JSON. Restituisce un riferimento alla
         lista 'commits' contenente i dizionari ottenuti.
        """

        assert whook is not None

        with open(GitlabIssueCommentWebhook._config_path, 'r') as f:
            configs = json.load(f)
        
        if os.environ['GITLAB_BASE_URL']:
            configs['base_url'] = os.environ['GITLAB_BASE_URL']


        webhook = {}
        webhook['app'] = 'gitlab'
        webhook['object_kind'] = whook['object_kind']
        # webhook['title'] = commit['message']
        webhook['project_id'] = configs['base_url'] + str(whook['project']['path_with_namespace'])
        #webhook['project_id'] = whook['project']['web_url']
        webhook['project_name'] = whook['project']['name']
        webhook['author'] = whook['user_name']
        webhook['commits'] = whook['commits']
        webhook['commits_count'] = whook['total_commits_count']
        webhook['repository'] = whook['repository']['name']

        # commits = []
        # for commit in whook['commits']:


        #     webhook['added'] = []
        #     for content in commit['added']:
        #         webhook['added'].append(content)
        #     commits.append(webhook)

        #     webhook['modified'] = []
        #     for content in commit['modified']:
        #         webhook['modified'].append(content)
        #     commits.append(webhook)

        #     webhook['removed'] = []
        #     for content in commit['removed']:
        #         webhook['removed'].append(content)
        #     commits.append(webhook)

        return webhook
