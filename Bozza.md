# Bozze nuovi casi d'uso

### UC1: Redmine segnala apertura issue a producer Redmine (`Project`, `Tracker`, `Subject`, `[Description]`, `Proirity`, `Status`, `[Assegnee]`)
* **Titolo**: Redmine segnala apertura issue al Producer Redmine
* **Attori primari**: Redmine
* **Attori secondari**: -
* **Descrizione**: sistema Producer Redmine ed è interno al sistema
Butterfly. L'apertura di una issue in un particolare progetto su Redmine
contiene i seguenti campi di interesse:
    * Tracker
    * Subject
    * Status
    * Priority e, opzionalmente:
        * Description

* **PRE**: Viene aperta una issue su Redmine
* **POST**: Il Producer Redmine ha ricevuto una segnalazione da Redmine
* **Estensioni**: -

### UC2: GitLab segnala apertura issue al Producer GitLab (`Title`, `[Label, Milestone, Assignee, Due Date]`)

* **Titolo**: GitLab segnala apertura issue al Producer GitLab
* **Attori primari**: GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Producer GitLab ed è interno al sistema
Butterfly. L'invio di una segnalazione avviene da parte di GitLab
(~tramite webhook). L'apertura di una issue su GitLab contiene:
    * Title e, opzionalmente:
        * Label
        * Milestone
        * Assegnee
        * Due Date

* **PRE**: Viene aperta una issue su GitLab
* **POST**: Il Producer GitLab ha ricevuto una segnalazione da GitLab
* **Estensioni**: -

### UCX: Gitlab segnala la modifica di una issue al Producer Gitlab

* **Titolo**: GitLab segnala la modifica di una issue al Producer GitLab
* **Attori primari**: GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Producer GitLab ed è interno al sistema
Butterfly. L'invio di una segnalazione avviene da parte di GitLab
tramite webhook, quando una issue viene modificata. 


<!-- L'apertura di una issue su GitLab contiene:
    * Title e, opzionalmente:
        * Label
        * Milestone
        * Assegnee
        * Due Date -->

* **PRE**: Viene modificata una issue già aperta su un progetto di GitLab
* **POST**: Il Producer GitLab ha ricevuto una segnalazione da GitLab
* **Estensioni**: -

### UCX.1: GitLab segnala la modifica di label di una issue al Producer GitLab

* **Titolo**: GitLab segnala la modifica di label di una issue al Producer GitLab
* **Attori primari**: GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Producer GitLab ed è interno al sistema
Butterfly. L'invio di una segnalazione avviene da parte di GitLab
tramite webhook. La modifica delle label di una issue già aperta
comporta la preservazione del messaggio.


<!-- L'apertura di una issue su GitLab contiene:
    * Title e, opzionalmente:
        * Label
        * Milestone
        * Assegnee
        * Due Date -->

* **PRE**: Viene modificata una issue già aperta su un progetto di GitLab
* **POST**: Il Producer GitLab ha ricevuto una segnalazione da GitLab
* **Estensioni**: -

### UCX.2: GitLab segnala la modifica del titolo di una issue al Producer GitLab

* **Titolo**: GitLab segnala la modifica del titolo di una issue al Producer GitLab
* **Attori primari**: GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Producer GitLab ed è interno al sistema
Butterfly. L'invio di una segnalazione avviene da parte di GitLab
tramite webhook. La modifica del titolo di una issue già aperta
comporta la preservazione del messaggio.


<!-- L'apertura di una issue su GitLab contiene:
    * Title e, opzionalmente:
        * Label
        * Milestone
        * Assegnee
        * Due Date -->

* **PRE**: Viene modificata una issue già aperta su un progetto di GitLab
* **POST**: Il Producer GitLab ha ricevuto una segnalazione da GitLab
* **Estensioni**: -

### UCX.3: GitLab segnala la modifica di campi non d'interesse di una issue al Producer GitLab

* **Titolo**: GitLab segnala la modifica di campi non d'interesse al Producer GitLab
* **Attori primari**: GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Producer GitLab ed è interno al sistema
Butterfly. L'invio di una segnalazione avviene da parte di GitLab
tramite webhook. La modifica del titolo di una issue già aperta
comporta la preservazione del messaggio.


<!-- L'apertura di una issue su GitLab contiene:
    * Title e, opzionalmente:
        * Label
        * Milestone
        * Assegnee
        * Due Date -->

* **PRE**: Viene modificata una issue già aperta su un progetto di GitLab
* **POST**: Il Producer GitLab ha ricevuto una segnalazione da GitLab e il messaggio viene scartato
* **Estensioni**: -

### UC3: GitLab segnala commit a Producer GitLab (`Commit message(la presenza di keyword non è obbligatoria)`)

* **Titolo**: GitLab segnala immissione (?) commit al Producer GitLab
* **Attori primari**: GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Producer GitLab ed è interno al sistema Butterfly. L'invio di una segnalazione avviene da parte di GitLab (~tramite webhook). Il messaggio può contenere keyword. Se non ne è presente alcuna, il messaggio verrà catalogato sotto la label speciale `unknown`.
* **PRE**: Viene immesso (?) un commit su GitLab
* **POST**: Il Producer GitLab ha ricevuto un messaggio (o segnalazione?) da GitLab
* **Estensioni**: -

### UC4: Producer Redmine invia messaggio al Gestore Personale

* **Titolo**: Producer Redmine invia messaggio al Gestore Personale
* **Attori primari**: Producer Redmine
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer Redmine, dopo aver ricevuto una determinata segnalazione da Redmine, rielabora il messaggio (come è fatto?) e la manda al Gestore Personale.  
Il messaggio finale, una volta terminata l'elaborazione, conterrà i campi:
* Project
* Topic
* Subject e, opzionalmente:
    * Description
* **PRE**: il Producer Redmine ha ricevuto una segnalazione di apertura issue da Redmine.
* **POST**: il Producer Redmine ha rielaborato e inviato al Gestore Personale il messaggio.
* **Estensioni**: -

### UC5: Producer GitLab invia messaggio al Gestore Personale

* **Titolo**: Producer GitLab invia messaggio al Gestore Personale
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer GitLab, dopo aver ricevuto una determinata segnalazione da GitLab, elabora un messaggio (come è fatto?) da inviare al Gestore Personale.  
Il messaggio finale, una volta elaborato, conterrà i campi:
* Project
* Topic
* Subject e, opzionalmente:
    * Description
* **PRE**: il Producer GitLab ha ricevuto una segnalazione di apertura issue da GitLab.
* **POST**: il Producer GitLab ha inviato al Gestore Personale il messaggio.
* **Estensioni**: -


### UC6: Gestore Personale inserisce il messaggio nella coda Telegram
* **Titolo**: Producer GitLab invia messaggio al Gestore Personale
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer GitLab, dopo aver ricevuto una determinata segnalazione da GitLab, elabora un messaggio (come è fatto?) da inviare al Gestore Personale.
* **PRE**: il Producer GitLab ha ricevuto una segnalazione di apertura issue da GitLab.
* **POST**: il Producer GitLab ha inviato al Gestore Personale il messaggio.
* **Estensioni**: -

### UC7: Dispatcher invia messaggio al Consumer E-mail


<!--
### UC6: Consumer Telegram invia messaggio a Telegram

### UC7: Consumer email invia messaggio a E-mail
!-->

## Alternative

Creare un caso d'uso per ogni coppia Producer-Consumer
* Problema: complessità esponenziale

# a

* wontfix
* bug
* DLQ
* email - consumer
* telegram - consumer

## Sottosistemi

* Producer Redmine
* Producer Gitlab
* Gestore Personale
* Coda Telegram
* Coda email