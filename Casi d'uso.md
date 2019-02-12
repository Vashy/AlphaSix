# Bozze nuovi casi d'uso

### UC1: Redmine segnala apertura issue a Producer Redmine
<!-- (`Project`, `Tracker`, `Subject`, `[Description]`, `Proirity`, `Status`, `[Assegnee]`) -->
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
        * Assegnee (da decidere: potrebbe essere utile per inviare la notifica solo all'assegnato)

* **PRE**: Viene aperta una issue su Redmine
* **POST**: Il Producer Redmine ha ricevuto una segnalazione da Redmine
* **Estensioni**: -

### UC2: GitLab segnala apertura issue al Producer GitLab 
<!-- (`Title`, `[Label, Milestone, Assignee, Due Date]`) -->

* **Titolo**: GitLab segnala apertura issue al Producer GitLab
* **Attori primari**: GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Producer GitLab ed è interno al sistema
Butterfly. L'invio di una segnalazione avviene da parte di GitLab
tramite webhook. L'apertura di una issue su GitLab contiene:
    * Title e, opzionalmente:
        * Label (0 a n)
        * Milestone
        * Assegnee (0 a n) (da decidere: potrebbe essere utile per inviare la notifica solo all'assegnato)
        * Due Date

* **PRE**: Viene aperta una issue su GitLab
* **POST**: Il Producer GitLab ha ricevuto una segnalazione da GitLab
* **Estensioni**: -

### UC3: Gitlab segnala la modifica di una issue al Producer Gitlab

* **Titolo**: GitLab segnala la modifica di una issue al Producer GitLab
* **Attori primari**: GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Producer GitLab ed è interno al sistema
Butterfly. L'invio di una segnalazione avviene da parte di GitLab
tramite webhook, quando una issue viene modificata.
* **PRE**: Viene modificata una issue già aperta su un progetto di GitLab
* **POST**: Il Producer GitLab ha ricevuto una segnalazione da GitLab
* **Estensioni**: -

### UC4: GitLab segnala evento di push a Producer GitLab 
<!-- (`Commit message(la presenza di keyword non è obbligatoria)`) -->
* **Titolo**: GitLab segnala evento di push al Producer GitLab
* **Attori primari**: GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Producer GitLab ed è interno al sistema Butterfly. L'invio di una segnalazione avviene da parte di GitLab (~tramite webhook). L'evento di push può essere composto da uno o più commit (campi del messaggio ottenuti dal webhook?).
* **PRE**: Viene effettuato un push su GitLab
* **POST**: Il Producer GitLab ha ricevuto un messaggio (o segnalazione?) da GitLab
* **Estensioni**: -

### UC5: Producer Redmine invia messaggio al Gestore Personale

* **Titolo**: Producer Redmine invia messaggio al Gestore Personale
* **Attori primari**: Producer Redmine
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer Redmine, dopo aver ricevuto una segnalazione da Redmine, elabora il messaggio (come è fatto?) e la manda al Gestore Personale.  
Il messaggio finale, una volta terminata l'elaborazione, conterrà i campi:
    * Project
    * Topic
    * Subject e, opzionalmente:
        * Description
* **PRE**: il Producer Redmine ha ricevuto una segnalazione da Redmine.
* **POST**: il Producer Redmine ha elaborato e inviato al Gestore Personale il messaggio.
* **Estensioni**: -

### UC5.1: Producer Redmine invia messaggio di apertura issue al Gestore Personale

* **Titolo**: Producer Redmine invia messaggio di apertura issue al Gestore Personale
* **Attori primari**: Producer Redmine
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer Redmine, dopo aver ricevuto una segnalazione di apertura issue (o Issue Event?) da Redmine, elabora il messaggio e lo manda al Gestore Personale.  
Il messaggio finale, una volta terminata l'elaborazione, conterrà i campi:
    * Project
    * Topic
    * Subject e, opzionalmente:
        * Description
* **PRE**: il Producer Redmine ha ricevuto una segnalazione da Redmine.
* **POST**: il Producer Redmine ha elaborato e inviato al Gestore Personale il messaggio di apertura issue.
* **Estensioni**: -

### UC5.2: Producer Redmine invia messaggio di modifica issue al Gestore Personale

* **Titolo**: Producer Redmine invia messaggio di modifica issue al Gestore Personale
* **Attori primari**: Producer Redmine
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer Redmine, dopo aver ricevuto una segnalazione di modifica issue (o Issue Event?) da Redmine, elabora il messaggio e lo manda al Gestore Personale.  
Il messaggio finale, una volta terminata l'elaborazione, conterrà i campi:
    * Project
    * Topic
    * Subject e, opzionalmente:
        * Description
* **PRE**: il Producer Redmine ha ricevuto una segnalazione da Redmine.
* **POST**: il Producer Redmine ha elaborato e inviato al Gestore Personale il messaggio di modifica issue.
* **Estensioni**: -

### UC6: Producer GitLab invia messaggio al Gestore Personale

* **Titolo**: Producer GitLab invia messaggio al Gestore Personale
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer GitLab, dopo aver ricevuto una segnalazione da GitLab, elabora un messaggio da inviare al Gestore Personale.
<!-- Il messaggio finale, una volta elaborato, conterrà i campi:
    * Project
    * Topic
    * Subject e, opzionalmente:
        * Description
        * Due date
        * Milestone
        * Assegnee -->
* **PRE**: il Producer GitLab ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer GitLab ha inviato al Gestore Personale il messaggio elaborato.
* **Estensioni**: -

### UC6.1: Producer GitLab invia messaggio di commit al Gestore Personale

* **Titolo**: Producer GitLab invia uno o più messaggi di commit al Gestore Personale
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer GitLab, dopo aver ricevuto una segnalazione di push da GitLab, elabora un messaggio per commit che verrà catalogato sotto il Topic "commits".
Il messaggio elaborato conterrà i campi:
    * Project
    * Topic (che sarà sempre "commits")
    * Message
* **PRE**: il Producer GitLab ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer GitLab ha inviato al Gestore Personale uno o più messaggi elaborati di commit.
* **Estensioni**: -

### UC6.2: Producer GitLab invia messaggio di issue al Gestore Personale

* **Titolo**: Producer GitLab invia messaggio di issue al Gestore Personale
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer GitLab, dopo aver ricevuto una segnalazione di issue da GitLab, controlla se la issue è appena stata creata o si tratta di una modifica di una issue preesistente.
Il messaggio elaborato, una volta elaborato, conterrà i campi:
    * Project
    * Topic
    * Subject e, opzionalmente:
        * Description
        * Due date (?)
        * Milestone (?)
        * Assegnee (?)
* **PRE**: il Producer GitLab ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer GitLab ha inviato al Gestore Personale il messaggio elaborato.
* **Estensioni**: -

### UC6.2.1: Producer GitLab invia messaggio di una nuova issue al Gestore Personale

* **Titolo**: Producer GitLab invia messaggio di una nuova issue al Gestore Personale
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer GitLab, dopo aver ricevuto una segnalazione di una nuova issue da GitLab, elabora il messaggio che conterrà i campi:
    * Project
    * Topic
    * Subject e, opzionalmente:
        * Description
        * Due date (?)
        * Milestone (?)
        * Assegnee (?)
* **PRE**: il Producer GitLab ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer GitLab ha inviato al Gestore Personale il messaggio elaborato di nuova issue.
* **Estensioni**: -

### UC6.2.2: Producer GitLab invia messaggio di modifica di una issue al Gestore Personale

* **Titolo**: Producer GitLab invia messaggio di modifica issue al Gestore Personale
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer GitLab, dopo aver ricevuto una segnalazione di modifica di una issue da GitLab, controlla se sono stati modificati i campi `Label` o `Title`. In caso positivo, viene inviato un messaggio elaborato al Gestore Personale, il quale conterrà:
* Project
* Topic
* Subject e, opzionalmente:
    * Description
    * Due date (?)
    * Milestone (?)
    * Assegnee (?)

* **PRE**: il Producer GitLab ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer GitLab ha inviato al Gestore Personale il messaggio elaborato di modifica issue.
* **Estensioni**: UC6.2.3

### UC6.2.3: Producer GitLab scarta i messaggi non validi

* **Titolo**: Producer GitLab scarta i messaggi non validi
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: Il Producer GitLab, dopo aver ricevuto una segnalazione di una modifica issue da GitLab, controlla se sono state modificati i campi `Label` o `Title`. In caso negativo, il messaggio viene scartato. 
* **PRE**: il Producer GitLab ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer GitLab ha scartato il messaggio
* **Estensioni**: -

### UC7: Gestore Personale inserisce il messaggio finale nella coda Telegram

* **Titolo**: Gestore Personale inserisce il messaggio finale nella coda Telegram
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema coda Telegram ed è interno al sistema
Butterfly. Il Gestore Personale, dopo aver ricevuto il messaggio
elaborato dai Producer Redmine o GitLab, valuta il campo Topic del
messaggio, controlla chi è iscritto a quel Topic, se la persona è
disponibile, e se vuole ricevere il messaggio tramite Telegram.
Se tutte queste condizioni sono verificate, viene preparato il messaggio
finale da inviare all'utente e inserito nella coda Telegram.
* **PRE**: il Gestore Personale ha ricevuto il messaggio elaborato dai Producer Redmine o GitLab.
* **POST**: Il Gestore Personale ha inserito il messaggio finale nella coda Telegram.
* **Estensioni**: -

### UC8: Gestore Personale inserisce il messaggio finale nella coda email

* **Titolo**: Gestore Personale inserisce il messaggio finale nella coda email
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema coda email ed è interno al sistema
Butterfly. Il Gestore Personale, dopo aver ricevuto il messaggio
elaborato dai Producer Redmine o GitLab, valuta il campo Topic del
messaggio, controlla chi è iscritto a quel Topic, se la persona è
disponibile, e se vuole ricevere il messaggio tramite email.
Se tutte queste condizioni sono verificate, viene preparato il messaggio
finale da inviare all'utente e inserito nella coda email.
* **PRE**: il Gestore Personale ha ricevuto il messaggio elaborato dai Producer Redmine o GitLab.
* **POST**: Il Gestore Personale ha inserito il messaggio finale nella coda email.
* **Estensioni**: -

### UC8: Consumer Telegram preleva il messaggio finale dalla coda Telegram

* **Titolo**: Consumer Telegram preleva il messaggio finale dalla coda Telegram
* **Attori primari**: Consumer Telegram
* **Attori secondari**: -
* **Descrizione**: sistema coda Telegram ed è interno al sistema
Butterfly. Il Consumer Telegram preleva dalla coda Telegram il messaggio
finale per poterlo inoltrare agli utenti di Telegram interessati.
* **PRE**: la coda Telegram contiene almeno un messaggio da prelevare.
* **POST**: Il messaggio finale è stato prelevato con successo.
* **Estensioni**: -

### UC9: Consumer email preleva il messaggio della coda email

* **Titolo**: Gestore Personale inserisce il messaggio finale nella coda email
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema coda email ed è interno al sistema
Butterfly. Il Consumer email preleva dalla coda email il messaggio
finale per poterlo inoltrare agli utenti di email interessati.
* **PRE**: la coda email contiene almeno un messaggio da prelevare.
* **POST**: Il messaggio finale è stato prelevato con successo.
* **Estensioni**: -

### UC10: Utente

## Alternative

Creare un caso d'uso per ogni coppia Producer-Consumer
* Problema: complessità esponenziale

## Sottosistemi

* Producer Redmine
* Producer Gitlab
* Gestore Personale
* Coda Telegram
* Coda email

## Utente

* utenti - UC accesso/UC-Aggiunta nuovo utente
  * Nome - UC Inserimento nome
  * Cognome - UC Inserimento cognome
  * Contatto email - UC Aggiunta contatto email
  * Contatto telegram - UC Aggiunta contatto telegram
* progetti - UC Aggiunta/rimozione
* label => topic - AUTO - Decidere dove?
* Ex UC6: Aggiunta/rimozione preferenze:
  * Iscrizione a topic
  * Disiscrizione da topic
  * Date indisponibilità
  * Aggiunta/rimozione keywords
  * Aggiunta/rimozione preferenza progetti (?)

Configurazioni?

## GitLab Issue Event

* `obj["object_kind"]`
* `obj["project"]["id"]/obj["object_attributes"]["project_id"]`
* `obj["project"]["name"]`
* `obj["assignees"][k]["username"]`
* `obj["object_attributes"]["action"]` (se ="close", da scartare)
* `obj["object_attributes"]["description"]`
* `obj["labels"][k]["title"]`
* `obj["labels"][k]["project_id"]`
* `obj["changes"]["title"]`
* `obj["changes"]["labels"]["previous"][k]["title"]`
* `obj["changes"]["labels"]["current"][k]["title"]`

## GitLab Push Event

* `obj["object_kind"] = "push"`
* `obj["user_id"]`
* `obj["user_username"]`
* `obj["project_id"]`
* `obj["commits"][k]["id"]`
* `obj["commits"][k]["message"]`
* `obj["commits"][k]["timestamp"]`
* `obj["commits"][k]["author"]["name"]`
* `obj["total_commits_count"]`

## Redmine Issue Opened Event
(Plugin: https://github.com/suer/redmine_webhook)

* `obj["payload"]["issue"]["priority"]["name"]`
* `obj["payload"]["issue"]["tracker"]["name"]`
* `obj["payload"]["issue"]["subject"]`
* `obj["payload"]["issue"]["status"]["name"]`
* `obj["payload"]["issue"]["description"]`
* `obj["payload"]["issue"]["project"]["id"]`
* `obj["payload"]["issue"]["project"]["name"]`
* `obj["payload"]["issue"]["action"]`