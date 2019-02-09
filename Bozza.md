# Bozze nuovi casi d'uso

### UC1: Redmine segnala apertura issue a producer Redmine (`Project`, `Tracker`, `Subject`, `[Description]`, `Proirity`)
* **Titolo**: Redmine segnala apertura issue al Producer Redmine
* **Attori primari**: Redmine
* **Attori secondari**: -
* **Descrizione**: sistema Producer Redmine ed è interno al sistema Butterfly. L'invio di una segnalazione avviene da parte di Redmine (~tramite webhook). Il messaggio deve contenere:
    * Il titolo del progetto
    * Tracker
    * Subject
    * Priority e, opzionalmente
    * Description
* **PRE**: Viene aperta una issue su Redmine
* **POST**: Il Producer Redmine ha ricevuto una segnalazione da Redmine
* **Estensioni**: -

### UC2: GitLab segnala apertura issue al Producer GitLab (`Title`, `Label`, `[Milestone, Assignee, Due Date]`)

* **Titolo**: GitLab segnala apertura issue al Producer GitLab
* **Attori primari**: GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Producer GitLab ed è interno al sistema Butterfly. L'invio di una segnalazione avviene da parte di GitLab (~tramite webhook). Il messaggio deve contenere:
    * Title
    * Label e, opzionalmente:
        * Milestone
        * Assegnee
        * Due Date
* **PRE**: Viene aperta una issue su GitLab
* **POST**: Il Producer GitLab ha ricevuto una segnalazione da GitLab
* **Estensioni**: -

### UC3: GitLab segnala commit a producer GitLab (`Commit message(la presenza di keyword non è obbligatoria)`)

* **Titolo**: GitLab segnala immissione (?) commit al Producer GitLab
* **Attori primari**: GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Producer GitLab ed è interno al sistema Butterfly. L'invio di una segnalazione avviene da parte di GitLab (~tramite webhook). Il messaggio può contenere keyword. Se non ne è presente alcuna, il messaggio verrà catalogato sotto la label speciale `unknown`.
* **PRE**: Viene immesso (?) un commit su GitLab
* **POST**: Il Producer GitLab ha ricevuto un messaggio (o segnalazione?) da GitLab
* **Estensioni**: -

### UC4: Producer Redmine invia messaggio al Dispatcher

* **Titolo**: Producer Redmine invia messaggio al "Consumer Dispatcher" (o sistema Consumer?)
* **Attori primari**: Producer Redmine
* **Attori secondari**: -
* **Descrizione**: sistema "Consumer Dispatcher" ed è interno al sistema Butterfly. Il Producer Redmine, dopo aver ricevuto una determinata segnalazione da Redmine, la inoltra al Consumer Dispatcher.
* **PRE**: il Producer Redmine ha ricevuto una segnalazione di apertura issue da Redmine.
* **POST**: il Producer Redmine ha inviato al Consumer Dispatcher il messaggio.
* **Estensioni**: -

### UC5: Producer GitLab invia messaggio al Dispatcher

* **Titolo**: Producer GitLab invia messaggio al "Consumer Dispatcher" (o sistema Consumer?)
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema "Consumer Dispatcher" ed è interno al sistema Butterfly. Il Producer GitLab, dopo aver ricevuto una determinata segnalazione da GitLab, la inoltra al Consumer Dispatcher.
* **PRE**: il Producer GitLab ha ricevuto una segnalazione di apertura issue da GitLab.
* **POST**: il Producer GitLab ha inviato al Consumer Dispatcher il messaggio.
* **Estensioni**: -


### UC6: Dispatcher invia messaggio al Consumer Telegram


### UC7: Dispatcher invia messaggio al Consumer E-mail


<!--
### UC6: Consumer Telegram invia messaggio a Telegram

### UC7: Consumer email invia messaggio a E-mail
!-->

## Alternative

Creare un caso d'uso per ogni coppia Producer-Consumer
* Problema: complessità esponenziale
