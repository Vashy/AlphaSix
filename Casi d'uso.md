# Bozze nuovi casi d'uso

### UC1: Redmine segnala apertura issue a Producer Redmine (`Project`, `Tracker`, `Subject`, `[Description]`, `Proirity`, `Status`, `[Assegnee]`)
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
tramite webhook. L'apertura di una issue su GitLab contiene:
    * Title e, opzionalmente:
        * Label
        * Milestone
        * Assegnee
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

### UC3: GitLab segnala commit a Producer GitLab (`Commit message(la presenza di keyword non è obbligatoria)`)
<!-- Producer ha accesso al database!! -->
* **Titolo**: GitLab segnala immissione (?) commit al Producer GitLab
* **Attori primari**: GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Producer GitLab ed è interno al sistema Butterfly. L'invio di una segnalazione avviene da parte di GitLab (~tramite webhook). Il messaggio può contenere keyword.
<!-- Se non ne è presente alcuna, il messaggio verrà catalogato sotto la label speciale `unknown`. -->
* **PRE**: Viene immesso (?) un commit su GitLab
* **POST**: Il Producer GitLab ha ricevuto un messaggio (o segnalazione?) da GitLab
* **Estensioni**: -

### UCY: Producer Redmine invia messaggio al Gestore Personale

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
    * Due date
    * Milestone
    * Assegnee
* **PRE**: il Producer GitLab ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer GitLab ha inviato al Gestore Personale il messaggio elaborato.
* **Estensioni**: -

### UC5.1: Producer GitLab invia messaggio di commit al Gestore Personale
<!-- Come UC3, condivisione di risorse -->
* **Titolo**: Producer GitLab invia messaggio di commit al Gestore Personale
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer GitLab, dopo aver ricevuto una segnalazione di commit da GitLab, controlla se ci sono keyword all'interno del messaggio, se dovessero esserci vengono inserite nel campo topic altrimenti vengono assegnate al topic di default "unknown".  
Il messaggio finale, una volta elaborato, conterrà i campi:
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

### UC5.2: Producer GitLab invia messaggio di issue al Gestore Personale

* **Titolo**: Producer GitLab invia messaggio di issue al Gestore Personale
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer GitLab, dopo aver ricevuto una segnalazione di issue da GitLab, controlla se la issue è appena stata creata o si tratta di una modifica di una issue preesistente.
Il messaggio finale, una volta elaborato, conterrà i campi:
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

### UC5.2.1: Producer GitLab invia messaggio di una nuova issue al Gestore Personale

* **Titolo**: Producer GitLab invia messaggio di una nuova issue al Gestore Personale
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer GitLab, dopo aver ricevuto una segnalazione di una nuova issue da GitLab, elabora il messaggio che, una volta elaborato, conterrà i campi:
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

### UC5.2.2: Producer GitLab invia messaggio di modifica di una issue al Gestore Personale

* **Titolo**: Producer GitLab invia messaggio di una nuova issue al Gestore Personale
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema Butterfly. Il Producer GitLab, dopo aver ricevuto una segnalazione di una nuova modifica di una issue da GitLab, controlla se sono stati modificati i campi 
`Label` o `Title`. In caso positivo, viene inviata un messaggio elaborato al Gestore Personale, il quale conterrà:
* Project
* Topic
* Subject e, opzionalmente:
    * Description
    * Due date (?)
    * Milestone (?)
    * Assegnee (?)

* **PRE**: il Producer GitLab ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer GitLab ha inviato al Gestore Personale il messaggio elaborato.
* **Estensioni**: UC5.2.3

### UC5.2.3: Producer GitLab scarta i messaggi non validi

* **Titolo**: Producer GitLab invia messaggio di una nuova issue al Gestore Personale
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Gestore Personale ed è interno al sistema 
Butterfly. Il Producer GitLab, dopo aver ricevuto una segnalazione di una 
modifica issue da GitLab. 
* Project
* Topic
* Subject e, opzionalmente:
    * Description
    * Due date
    * Milestone
    * Assegnee
* **PRE**: il Producer GitLab ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer GitLab ha inviato al Gestore Personale il messaggio elaborato.
* **Estensioni**: -

### UC6: Gestore Personale inserisce il messaggio finale nella coda Telegram

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

### UC7: Gestore Personale inserisce il messaggio finale nella coda email

* **Titolo**: Gestore Personale inserisce il messaggio finale nella coda email
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: sistema coda Telegram ed è interno al sistema
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
