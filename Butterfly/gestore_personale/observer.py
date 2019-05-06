"""
File: consumer.py
Data creazione: 2019-03-15

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
    Nicola Carlesso, nicolacarlesso@outlook.it
"""

from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def update(self, resource: str, request_type: str, url: str, msg: str):
        pass


class Subject(ABC):

    def addObserver(self, obs: Observer):
        if not hasattr(self, '_lst'):
            self._lst = []
        if obs not in self._lst:
            self._lst.append(obs)

    @abstractmethod
    def notify(self, request_type: str, resource: str, url: str, msg: str):
        pass
