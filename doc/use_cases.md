# Bozze nuovi casi d'uso

### UC1: Redmine o GitLab inviano una segnalazione a Butterfly che la inoltra ad un utente Telegram o ad un indirizzo Email
* **Titolo**: Redmine o GitLab inviano una segnalazione a Butterfly che la inoltra ad un utente Telegram o ad un indirizzo Email
* **Attori primari**: Redmine, Telegram
* **Attori secondari**: Telegram, Email
* **Descrizione**: sistema Producer Redmine ed è Butterfly. Redmine segnala a Butterfly l'apertura o la modifica di una issue di un particolare progetto. Lo stesso lo può fare GitLab segnalando l'apertura o modifica di una issue, con in più la segnalazione di un evento di push. In base alle impostazioni del Gestore Personale, tale segnalazione sarà inoltrata ad uno o più utent Telegram o ad uno o più indirizzi Email.
* **PRE**: Viene aperta o modificata una issue su Redmine, aperta o modificata una issue su GitLab, oppure viene effettuata un azione di push su GitLab.
* **POST**: L'utente Telegram o l'indirizzo Email selezionati ricevono la notifica delle segnalazione inviata da Redmine o GitLab
* **Estensioni**: -

### UC2: Redmine segnala apertura issue a Producer Redmine
<!-- (`Project`, `Tracker`, `Subject`, `[Description]`, `Proirity`, `Status`, `[Assignee]`) -->
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
        * Assignee (da decidere: potrebbe essere utile per inviare la notifica solo all'assegnato)

* **PRE**: Viene aperta una issue su Redmine
* **POST**: Il Producer Redmine ha ricevuto una segnalazione da Redmine
* **Estensioni**: -

### UC3: Redmine segnala la modifica di una issue al Producer Redmine

* **Titolo**: Redmine segnala la modifica di una issue al Producer Redmine
* **Attori primari**: Redmine
* **Attori secondari**: -
* **Descrizione**: sistema Producer Redmine ed è interno al sistema
Butterfly. Viene inviata una segnalazione da parte di GitLab
tramite webhook nel momento una issue già creata viene modificata.
* **PRE**: Viene modificata una issue già aperta su un progetto di Redmine
* **POST**: Il Producer Redmine ha ricevuto una segnalazione da Redmine
* **Estensioni**: -

### UC4: GitLab segnala apertura issue al Producer GitLab 
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
        * Assignee (0 a n) (da decidere: potrebbe essere utile per inviare la notifica solo all'assegnato)
        * Due Date

* **PRE**: Viene aperta una issue su GitLab
* **POST**: Il Producer GitLab ha ricevuto una segnalazione da GitLab
* **Estensioni**: -

### UC5: Gitlab segnala la modifica di una issue al Producer Gitlab

* **Titolo**: GitLab segnala la modifica di una issue al Producer GitLab
* **Attori primari**: GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Producer GitLab ed è interno al sistema
Butterfly. L'invio di una segnalazione avviene da parte di GitLab
tramite webhook, quando una issue viene modificata.
* **PRE**: Viene modificata una issue già aperta su un progetto di GitLab
* **POST**: Il Producer GitLab ha ricevuto una segnalazione da GitLab
* **Estensioni**: -

### UC6: GitLab segnala evento di push a Producer GitLab 
<!-- (`Commit message(la presenza di keyword non è obbligatoria)`) -->
* **Titolo**: GitLab segnala evento di push al Producer GitLab
* **Attori primari**: GitLab
* **Attori secondari**: -
* **Descrizione**: sistema Producer GitLab ed è interno al sistema Butterfly. L'invio di una segnalazione avviene da parte di GitLab (~tramite webhook). L'evento di push può essere composto da uno o più commit (campi del messaggio ottenuti dal webhook?).
* **PRE**: Viene effettuato un push su GitLab
* **POST**: Il Producer GitLab ha ricevuto un messaggio (o segnalazione?) da GitLab
* **Estensioni**: -

### UC7: Producer Redmine invia messaggio al Gestore Personale

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

### UC7.1: Producer Redmine invia messaggio di apertura issue al Gestore Personale

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

### UC7.2: Producer Redmine invia messaggio di modifica issue al Gestore Personale

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

### UC7.3: Producer Redmine scarta i messaggi non validi

* **Titolo**: Producer Redmine scarta i messaggi non validi
* **Attori primari**: Producer Redmine
* **Attori secondari**: -
* **Descrizione**: Il Producer Redmine, dopo aver ricevuto una segnalazione di una modifica issue da GitLab, controlla se è stato modificato il campo `Subject` . In caso negativo, il messaggio viene scartato.
* **PRE**: il Producer Redmine ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer Redmine ha scartato il messaggio
* **Estensioni**: -

### UC8: Producer GitLab invia messaggio al Gestore Personale

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
        * Assignee -->
* **PRE**: il Producer GitLab ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer GitLab ha inviato al Gestore Personale il messaggio elaborato.
* **Estensioni**: -

### UC8.1: Producer GitLab invia messaggio di commit al Gestore Personale

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

### UC8.2: Producer GitLab invia messaggio di issue al Gestore Personale

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
        * Assignee (?)
* **PRE**: il Producer GitLab ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer GitLab ha inviato al Gestore Personale il messaggio elaborato.
* **Estensioni**: -

### UC8.2.1: Producer GitLab invia messaggio di una nuova issue al Gestore Personale

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
        * Assignee (?)
* **PRE**: il Producer GitLab ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer GitLab ha inviato al Gestore Personale il messaggio elaborato di nuova issue.
* **Estensioni**: -

### UC8.2.2: Producer GitLab invia messaggio di modifica di una issue al Gestore Personale

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
    * Assignee (?)

* **PRE**: il Producer GitLab ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer GitLab ha inviato al Gestore Personale il messaggio elaborato di modifica issue.
* **Estensioni**: UC8.2.3

### UC8.2.3: Producer GitLab scarta i messaggi non validi

* **Titolo**: Producer GitLab scarta i messaggi non validi
* **Attori primari**: Producer GitLab
* **Attori secondari**: -
* **Descrizione**: Il Producer GitLab, dopo aver ricevuto una segnalazione di una modifica issue da GitLab, controlla se sono state modificati i campi `Label` o `Title`. In caso negativo, il messaggio viene scartato.
* **PRE**: il Producer GitLab ha ricevuto una segnalazione da GitLab.
* **POST**: il Producer GitLab ha scartato il messaggio
* **Estensioni**: -

### UC9: Gestore Personale invia il messaggio finale al Consumer Telegram

* **Titolo**: Gestore Personale invia il messaggio finale al Consumer Telegram
* **Attori primari**: Gestore Personale
* **Attori secondari**: -
* **Descrizione**: sistema è il producer Telegram ed è interno al sistema
Butterfly. Il Gestore Personale, dopo aver ricevuto il messaggio
elaborato dai Producer Redmine o GitLab, valuta il campo Topic del
messaggio, controlla chi è iscritto a quel Topic, se la persona è
disponibile, e se vuole ricevere il messaggio tramite Telegram.
Se tutte queste condizioni sono verificate, viene preparato il messaggio
finale da inviare all'utente e inviato al Consumer Telegram.
Il messaggio finale, una volta elaborato, conterrà i campi:
    * Id della chat del destinatario
    * Applicazione di provenienza
    * Ora di invio
    * Tipo di segnalazione (commit,issue)
    * Project
    * Topic
    * Subject e, opzionalmente:
        * Description
        * Due date
        * Milestone
        * Assignee
* **PRE**: il Gestore Personale ha ricevuto il messaggio elaborato dai Producer Redmine o GitLab.
* **POST**: Il Gestore Personale ha inviato il messaggio finale al Consumer Telegram.
* **Estensioni**: -

### UC10: Gestore Personale invia il messaggio finale al Consumer Email

* **Titolo**: Gestore Personale invia il messaggio finale al Consumer Email
* **Attori primari**: Gestore Personale
* **Attori secondari**: -
* **Descrizione**: sistema Consumer Email ed è interno al sistema
Butterfly. Il Gestore Personale, dopo aver ricevuto il messaggio
elaborato dai Producer Redmine o GitLab, valuta il campo Topic del
messaggio, controlla chi è iscritto a quel Topic, se la persona è
disponibile, e se vuole ricevere il messaggio tramite email.
Se tutte queste condizioni sono verificate, viene preparato il messaggio
finale da inviare al Consumer Email.
Il messaggio finale, una volta elaborato, conterrà i campi:
    * Email del destinatario
    * Applicazione di provenienza
    * Ora di invio
    * Tipo di segnalazione (commit,issue)
    * Project
    * Topic
    * Subject e, opzionalmente:
        * Description
        * Due date
        * Milestone
        * Assignee
* **PRE**: il Gestore Personale ha ricevuto il messaggio elaborato dai Producer Redmine o GitLab.
* **POST**: Il Gestore Personale ha inviato il messaggio finale al Consumer Email.
* **Estensioni**: -

### UC11: Consumer Telegram inoltra il messaggio finale al bot Telegram

* **Titolo**: Consumer Telegram inoltra il messaggio finale al bot Telegram
* **Attori primari**: Consumer Telegram
* **Attori secondari**: Telegram
* **Descrizione**: sistema è il bot Telegram ed è interno al sistema
Butterfly. Il Consumer Telegram inoltra il messaggio finale al bot Telegram, il quale notifica il destinatario finale attraverso Telegram.
* **PRE**: il Consumer Telegram ha ricevuto almeno un messaggio.
* **POST**: il bot Telegram ha ricevuto il messaggio finale con successo.
* **Estensioni**: -

### UC12: Consumer Email inoltra il messaggio finale al server Email

* **Titolo**: Consumer Email inoltra il messaggio finale al server Email
* **Attori primari**: Consumer Email
* **Attori secondari**: Email
* **Descrizione**: sistema server email ed è interno al sistema
Butterfly. Il Consumer Email inoltra il messaggio finale al server Email, il quale notifica il destinatario finale attraverso una Email.
* **PRE**: il Consumer Email ha ricevuto almeno un messaggio.
* **POST**: il server Email ha ricevuto il messaggio finale con successo.
* **Estensioni**: -

### UC13: Accesso

* **Titolo**: accesso.
* **Attori primari**: utente non acceduto.
* **Descrizione**: l’utente richiede di accedere al sistema attraverso un form dove inserisce l’nome utente.
* **PRE**: il sistema considera l’utilizzatore di esso come un utente non acceduto.
* **POST**: il sistema riconosce l’utilizzatore di esso come utente acceduto.
* **Estensioni**: -

### UC13.1: Accesso dell'utente nel sistema

* **Titolo**: accesso dell’utente nel sistema.
* **Attori primari**: utente non acceduto.
* **Descrizione**: l’utente attende l’accesso al sistema.
* **PRE**: il sistema riconosce l’utilizzatore come un utente non acceduto.
* **POST**: il sistema riconosce l'utente con successo.
* **Estensioni**: UC13.2

### UC13.1.1: Inserimento nome utente

* **Titolo**: inserimento nome utente.
* **Attori primari**: utente non acceduto.
* **Descrizione**: l’utente inserisce l’nome utente.
* **PRE**: il sistema offre l’interfaccia grafica adatta all’inserimento dell’nome utente.
* **POST**: l’utente ha inserito l’nome utente desiderato.
* **Estensioni**: UC13.2

### UC13.2 Errore nome utente inesistente

* **Titolo**: errore nome utente inesistente.
* **Attori primari**: utente non acceduto.
* **Descrizione**: l’utente viene avvisato che ha inserito uno nome utente errato.
* **PRE**: il sistema riceve una richiesta di accesso da parte di un utente che fornisce uno nome utente errato.
* **POST**: il sistema comunica all’utilizzatore l’errore.
* **Estensioni**: -

### UC14 Uscita del'utente dal sistema

* **Titolo**: Uscita del'utente dal sistema.
* **Attori primari**: utente acceduto.
* **Descrizione**: l'utente esce dal sistema ed ha la possibilità di rientrarci come un diverso utente o come lo stesso di prima.
* **PRE**: l'utente è all'interno del sistema.
* **POST**: l'utente si trova a poter accedere nuovamente nel sistema.
* **Estensioni**: -

### UC15: Aggiunta nuovo utente

* **Titolo**: Aggiunta nuovo utente.
* **Attori primari**: utente non registrato.
* **Descrizione**: l'utente non registrato aggiunge un nuovo utente nel sistema.
* **PRE**: un nuovo utente deve essere aggiunto nel sistema.
* **POST**: un utente con le credenziali inserite viene aggiunto al sistema.
* **Estensioni**:

### UC15.1 Utente aggiunto con successo

* **Titolo**: Utente aggiunto con successo.
* **Attori primari**: utente non registrato.
* **Descrizione**: un nuovo utente viene inserito con successo nel sistema.
* **PRE**: un nuovo utente deve essere aggiunto nel sistema.
* **POST**: un utente con le credenziali inserite viene aggiunto al sistema.
* **Estensioni**: UC15.2


* **Titolo**: Inserimento nome utente.
* **Attori primari**: utente non registrato.
* **Descrizione**: L'utente ha aggiunto il nome delle nuove credenziali (?)
* **PRE**: un nuovo utente deve essere aggiunto nel sistema.
* **POST**: il nome è stato inserito.
* **Estensioni**: UC15.2

### UC15.1.2 Inserimento cognome utente

* **Titolo**: Inserimento cognome utente.
* **Attori primari**: utente non registrato.
* **Descrizione**: L'utente ha aggiunto il cognome delle nuove credenziali (?)
* **PRE**: un nuovo utente deve essere aggiunto nel sistema.
* **POST**: il cognome è stato inserito.
* **Estensioni**: UC15.2

### UC15.1.3 Inserimento contatto email

* **Titolo**: Inserimento contatto email.
* **Attori primari**: utente non registrato.
* **Descrizione**: L'utente ha aggiunto il contatto email delle nuove credenziali (?)
* **PRE**: un nuovo utente deve essere aggiunto nel sistema.
* **POST**: il contatto email è stato inserito.
* **Estensioni**: UC15.2

### UC15.1.4 Inserimento contatto Telegram

* **Titolo**: Inserimento contatto Telegram.
* **Attori primari**: utente non registrato.
* **Descrizione**: L'utente ha aggiunto il contatto Telegram delle nuove credenziali (?)
* **PRE**: un nuovo utente deve essere aggiunto nel sistema.
* **POST**: il contatto Telegram è stato inserito.
* **Estensioni**: UC15.2

### UC15.2 Errore utente già presente nel sistema

* **Titolo**: errore utente già presente nel sistema.
* **Attori primari**: utente non registrato.
* **Descrizione**: l’utente viene avvisato che le nuove credenziali immesse non sono univoche. Questo avviene quando il contatto Telegram o email è già presente. 
* **PRE**: un nuovo utente deve essere aggiunto al sistema
* **POST**: il sistema comunica all’utilizzatore l’errore e l'utente non viene inserito.
* **Estensioni**: -

### UC16 Rimozione utente dal sistema

* **Titolo**: Rimozione utente dal sistema.
* **Attori primari**: utente.
* **Descrizione**: l'utente rimuove l'utente desiderato dal sistema inserendo la Email o il contatto Telegram dell'utente che si vuole rimuovere.
* **PRE**: un utente già presente deve essere rimosso nel sistema.
* **POST**: un utente viene rimosso dal sistema.
* **Estensioni**: -

### UC16.1 Rimozione avvenuta con successo

* **Titolo**: Rimozione utente dal sistema.
* **Attori primari**: utente.
* **Descrizione**: Il contatto email o Telegram desiderato è presente nel sistema, per cui la rimozione avviene con successo.
* **PRE**: un utente già presente deve essere rimosso nel sistema.
* **POST**: un utente con il contatto email o Telegram inserito viene rimosso dal sistema.
* **Estensioni**: UC16.2, UC16.3

### UC16.1.1 Inserimento contatto email

* **Titolo**: Inserimento contatto email.
* **Attori primari**: utente.
* **Descrizione**: L'utente ha aggiunto il contatto email relativo allo utente che vuole rimuovere.
* **PRE**: un utente già presente deve essere rimosso nel sistema.
* **POST**: il contatto email è stato inserito.
* **Estensioni**: UC16.2, UC16.3

### UC16.1.2 Inserimento contatto Telegram

* **Titolo**: Inserimento contatto Telegram.
* **Attori primari**: utente.
* **Descrizione**: L'utente ha aggiunto il contatto Telegram relativo allo utente che vuole rimuovere.
* **PRE**: un utente già presente deve essere rimosso nel sistema.
* **POST**: il contatto Telegram è stato inserito.
* **Estensioni**: UC16.2, UC16.3

### UC16.2 Errore contatto non presente nel sistema

* **Titolo**: errore contatto non presente nel sistema.
* **Attori primari**: utente.
* **Descrizione**: l’utente viene avvisato che il contatto inserito non è presente nel sistema.
* **PRE**: un utente già presente deve essere rimosso nel sistema.
* **POST**: il sistema comunica all’utilizzatore l’errore e nessun utente viene rimosso.
* **Estensioni**: -

### UC16.3 L'utente rimuove se stesso dal sistema

* **Titolo**: L'utente rimuove se stesso dal sistema.
* **Attori primari**: utente.
* **Descrizione**: l’utente inserisce i propri campi per rimuovere un utente dal sistema.
* **PRE**: un utente già presente deve essere rimosso nel sistema.
* **POST**: l'utente esce dal sistema perché non è più registrato con un messaggio dell'avvenuta disiscrizione.
* **Estensioni**: -

### UC17 Modifica utente

* **Titolo**: Modifica utente.
* **Attori primari**: utente.
* **Descrizione**: l’utente vuole modificare le informazioni relative a un utente.
* **PRE**: l'utente vuole modificare un utente già presente.
* **POST**: i campi dell'utente sono stati modificati correttamente.
* **Estensioni**: -

### UC17.1 Selezione utente ID

* **Titolo**: Selezione utente ID.
* **Attori primari**: utente.
* **Descrizione**: L'utente ha aggiunto il nuovo nome dello utente che vuole modificare
* **PRE**: l'utente vuole modificare un utente già presente.
* **POST**: lo utente ID è stato inserito.
* **Estensioni**: UC17.2

### UC17.1.1 Modifica utente avvenuta con successo

* **Titolo**: Modifica utente avvenuta con successo.
* **Attori primari**: utente.
* **Descrizione**: lo utente ID è presente nel sistema e ne vengono modificati i relativi campi con successo.
* **PRE**: l'utente vuole modificare un utente già presente.
* **POST**: lo utente è stato modificato con successo.
* **Estensioni**: UC17.2

### UC17.1.1.1 Inserimento del nuovo nome

* **Titolo**: Inserimento del nuovo nome.
* **Attori primari**: utente.
* **Descrizione**: L'utente aggiunge il nuovo nome relativo allo utente ID inserito che vuole modificare.
* **PRE**: l'utente vuole modificare un utente già presente.
* **POST**: il nome è stato inserito.
* **Estensioni**: UC17.2

### UC17.1.1.2 Inserimento del nuovo cognome

* **Titolo**: Inserimento del nuovo cognome.
* **Attori primari**: utente.
* **Descrizione**: L'utente aggiunge il nuovo cognome dello utente ID che vuole modificare.
* **PRE**: l'utente vuole modificare un utente già presente.
* **POST**: il cognome è stato inserito.
* **Estensioni**: UC17.2

### UC17.1.1.3 Inserimento nuovo contatto email

* **Titolo**: Inserimento nuovo contatto email.
* **Attori primari**: utente.
* **Descrizione**: L'utente aggiunge il nuovo contatto email relativo allo utente ID che vuole modificare.
* **PRE**: l'utente vuole modificare un utente già presente.
* **POST**: il contatto email è stato inserito.
* **Estensioni**: UC17.2

### UC17.1.1.4 Inserimento nuovo contatto Telegram

* **Titolo**: Inserimento nuovo contatto Telegram.
* **Attori primari**: utente.
* **Descrizione**: L'utente ha aggiunge il nuovo contatto Telegram relativo allo utente ID che vuole modificare.
* **PRE**: l'utente vuole modificare un utente già presente.
* **POST**: il contatto Telegram è stato inserito.
* **Estensioni**: UC17.2

### UC17.1.2 Errore nuovi dati dell'utente già esistenti

* **Titolo**: Errore nuovi dati dell'utente già esistenti
* **Attori primari**: utente.
* **Descrizione**: I nuovi campi che l'utente inserisce nella modifica sono già presenti nel sistema.
* **PRE**: l'utente vuole modificare un utente già presente.
* **POST**: il contatto Telegram è stato inserito.
* **Estensioni**: UC17.2

### UC17.2 Errore utente ID inesistente

* **Titolo**: errore utente ID inesistente.
* **Attori primari**: utente.
* **Descrizione**: l’utente viene avvisato che ha inserito un utente ID errato.
* **PRE**: l'utente vuole modificare un utente già presente.
* **POST**: il sistema comunica all’utente l’errore.
* **Estensioni**: -

### UC18 Aggiunta preferenze

* **Titolo**: aggiunta preferenze.
* **Attori primari**: utente.
* **Descrizione**: l’utente, date le varie opzioni per configurare Butterfly, aggiunge una preferenza tra Topic, giorni di calendario, piattaforma di messaggistica (Telegram o e-mail) preferita e la persona di fiducia che lo può sostituire.
* **PRE**: l’utente ha acceduto con le sue credenziali corrette nel sistema e non ha già selezionato tutte le preferenze possibili proposte da Butterfly.
* **POST**: la nuova configurazione contiene una o più preferenze in aggiunta rispetto a quella precedente.
* **Estensioni**: -

### UC18.1 Iscrizione Topic

* **Titolo**: iscrizione Topic.
* **Attori primari**: utente.
* **Descrizione**: data la lista di Topic presenti, l’utente ne seleziona uno o più a cui è interessato, ricevendone una notifica. I Topic sono divisi per categoria e comprendono etichette, progetto a cui sono legate e l'applicazione di provenienza: Redmine o GitLab.
* **PRE**: l’utente ha acceduto correttamente nel sistema e non ha già selezionato tutti i Topic possibili proposti da Butterfly.
* **POST**: il numero di Topic a cui è interessato l’utente è aumentato.
* **Estensioni**: -

### UC18.2 Aggiunta dei giorni di indisponibilità nel calendario

* **Titolo**: aggiunta dei giorni di indisponibilità nel calendario.
* **Attori primari**: utente.
* **Descrizione**: dato il calendario lavorativo, l’utente aggiunge uno o più giorni in cui non è reperibile e non vuole ricevere notifiche.
* **PRE**: l’utente ha acceduto correttamente nel sistema e non ha già selezionato tutti i giorni di calendario proposti da Butterfly.
* **POST**: il numero di giorni in cui l’utente non si rende disponibile è aumentato.
* **Estensioni**: -

### UC18.3 Aggiunta della piattaforma di messaggistica preferita

* **Titolo**: aggiunta della piattaforma di messaggistica preferita.
* **Attori** primari: utente.
* **Descrizione**: l’utente aggiunge la sua preferenza tra Telegram e email dove vuole ricevere le notifiche.
* **PRE**: l’utente ha acceduto correttamente nel sistema e non ha già selezionato tutte le piattaforme di messaggistica possibili proposte da Butterfly.
* **POST**: il numero di piattaforme di messaggistica selezionate dall’utente è aumentato.
* **Estensioni**: -

### UC18.4 Aggiunta persona di fiducia

* **Titolo**: aggiunta persona di fiducia.
* **Attori primari**: utente.
* **Descrizione**: l’utente aggiunge lo utente legato a un ID di sua preferenza a cui inoltrare i messaggi in caso di indisponibilità.
* **PRE**: l’utente ha acceduto con le sue credenziali corrette nel sistema e non ha già selezionato la persona a cui inoltrare le notifiche.
* **POST**: la preferenza viene aggiunta correttamente.
* **Estensioni**: UC18.5

### UC18.5 Errore ID persona di fiducia inesistente

* **Titolo**: Errore ID persona di fiducia inesistente.
* **Attori primari**: utente.
* **Descrizione**: l’utente viene avvisato che ha inserito un utente ID errato.
* **PRE**: l’utente ha acceduto con le sue credenziali corrette nel sistema e non ha già selezionato la persona a cui inoltrare le notifiche.
* **POST**: il sistema comunica all’utilizzatore l’errore di preferenza.
* **Estensioni**: -

### UC18.6 Aggiunta keyword per i push di GitLab

* **Titolo**: Aggiunta keyword per i push di GitLab.
* **Attori primari**: utente.
* **Descrizione**: l’utente aggiunge le keyword che vuole che siano contenute nei messaggi di commit dei push di cui vuole ricevere la notifica.
* **PRE**: l’utente ha acceduto con le sue credenziali corrette nel sistema.
* **POST**: nelle nuove configurazioni dell'utente selezionato sono presenti nuove keyword per ricevere notifiche da push di GitLab.
* **Estensioni**: -

### UC18.7 Errore keyword già esistente

* **Titolo**: Aggiunta keyword per i push di GitLab.
* **Attori primari**: utente.
* **Descrizione**: la keyword che vuole aggiungere l'utente è già registrata nel sistema.
* **PRE**: l’utente ha acceduto con le sue credenziali corrette nel sistema.
* **POST**: viene visualizzato un messaggio d'errore con indicato che la keyword selezionata è già presente nel sistema.
* **Estensioni**: -

### UC19 Rimozione preferenze

* **Titolo**: rimozione preferenza.
* **Attori primari**: utente.
* **Descrizione**: l’utente, dopo aver selezionato delle preferenze dalle opzioni di configurazione, ne rimuove una o più. Le preferenze consistono in Topic, date di calendario, piattaforma di messaggistica (Telegram e email) e persona di fiducia che lo può sostituire.
* **PRE**: l’utente ha eseguito l'accesso nel sistema ed è presente almeno una preferenza selezionata tra quelle proposte da Butterfly.
* **POST**: la nuova configurazione contiene una o più preferenze in meno rispetto a quella precedente.

### UC19.1 Disiscrizione Topic

* **Titolo**: disiscrizione Topic.
* **Attori primari**: utente.
* **Descrizione**: l’utente si disiscrive da uno o più Topic dai quali prima riceveva delle notifiche.
* **PRE**: l’utente ha acceduto correttamente nel sistema ed è presente almeno un Topic selezionato tra quelli proposti da Butterfly.
* **POST**: il numero di Topic a cui è iscritto l’utente è diminuito.
* **Estensioni**: -

### UC19.2 Rimozione di uno o più giorni di irreperibilità nel calendario

* **Titolo**: rimozione di uno o più giorni di irreperibilità nel calendario.
* **Attori primari**: utente.
* **Descrizione**: l’utente rimuove i giorni di calendario in cui precedentemente non era reperibile, tornando disponibile.
* **PRE**: l’utente ha acceduto correttamente nel sistema ed è presente almeno un giorno di calendario selezionato tra quelli proposti da Butterfly.
* **POST**: il numero di giorni di calendario in cui l’utente non è reperibile è diminuito.
* **Estensioni**: -

### UC19.3 Rimozione preferenza piattaforma di messaggistica

* **Titolo**: rimozione piattaforma di messaggistica.
* **Attori primari**: utente.
* **Descrizione**: l’utente rimuove una o più preferenze tra Telegram e email dalle quali non vuole più ricevere notifiche tramite Butterfly.
* **PRE**: l’utente ha acceduto correttamente nel sistema ed è presente almeno una piattaforma di messaggistica selezionata tra quelle proposte da Butterfly.
* **POST**: il numero di piattaforme di messaggistica da cui l’utente vuole ricevere notifiche è diminuito.
* **Estensioni**: -

### UC19.4 Rimozione persona di fiducia

* **Titolo**: rimozione persona di fiducia.
* **Attori primari**: utente.
* **Descrizione**: l’utente rimuove lo utente legato a un ID di sua preferenza a cui inoltrare i messaggi in caso di indisponibilità.
* **PRE**: l’utente ha eseguito l'accesso nel sistema ed è presente almeno un utente con l'ID selezionato tra quelle proposte da Butterfly.
* **POST**: la preferenza viene rimossa correttamente.
* **Estensioni**: UC19.5

### UC19.5 Errore ID persona di fiducia inesistente

* **Titolo**: Errore ID persona di fiducia inesistente.
* **Attori primari**: utente.
* **Descrizione**: l’utente viene avvisato che ha inserito un utente ID errato.
* **PRE**: l’utente ha acceduto con le sue credenziali corrette nel sistema e non ha già selezionato la persona a cui inoltrare le notifiche.
* **POST**: il sistema comunica all’utilizzatore l’errore di preferenza.
* **Estensioni**: -

### UC19.6 Rimozione con successo di keyword per i push di GitLab

* **Titolo**: Rimozione con successo di keyword per i push di GitLab.
* **Attori primari**: utente.
* **Descrizione**: l’utente seleziona e rimuove una o più keyword già presente nel sistema per non ricevere la notifica di push in cui i messaggi di commit contengono la keyword rimossa.
* **PRE**: l’utente ha acceduto con le sue credenziali corrette nel sistema.
* **POST**: nelle nuove configurazioni dell'utente selezionato sono state rimosse delle keyword precedentemente presenti.
* **Estensioni**: UC19.7

### UC19.7 Errore keyword da rimuovere non presente

* **Titolo**: Errore keyword da rimuovere non presente.
* **Attori primari**: utente.
* **Descrizione**: la keyword che l'utente intende rimuovere non è registrata nel sistema.
* **PRE**: l’utente ha acceduto con le sue credenziali corrette nel sistema.
* **POST**: viene visualizzato un messaggio d'errore con indicato che la keyword selezionata non è presente nel sistema.
* **Estensioni**: -

<!-- 
### UC18 Aggiunta nuovo progetto

No, perchè l'informazione viene raccolta dagli webhook.
In particolare, ogni segnalazione porta con se tutte le informazioni
relative a un progetto

* **Titolo**: Aggiunta nuovo progetto.
* **Attori primari**: utente.
* **Descrizione**: l'utente aggiunge un nuovo progetto nel sistema.
* **PRE**: un nuovo progetto deve essere aggiunto al sistema.
* **POST**: Il progetto è stato inserito nel sistema.
* **Estensioni**: -

### UC18.1 Aggiunta progetto avvenuta con successo

* **Titolo**: Aggiunta progetto avvenuta con successo.
* **Attori primari**: utente.
* **Descrizione**: un nuovo progetto viene inserito con successo nel sistema.
* **PRE**: un nuovo progetto deve essere aggiunto al sistema.
* **POST**: un progetto che non è già presente viene aggiunto al sistema.
* **Estensioni**: UC18.2, UC18.3

### UC18.1.1 Inserimento URL progetto

* **Titolo**: Inserimento URL progetto.
* **Attori primari**: utente.
* **Descrizione**: L'utente aggiunge l'URL del progetto che vuole aggiungere al sistema.
* **PRE**: un nuovo progetto deve essere aggiunto al sistema.
* **POST**: l'URL del progetto è stato inserito.
* **Estensioni**: -

### UC18.2 Errore progetto già presente nel sistema

* **Titolo**: Errore progetto già presente nel sistema.
* **Attori primari**: utente.
* **Descrizione**: l’utente viene avvisato che il progetto che vorrebbe aggiungere è già memorizzato nel sistema. 
* **PRE**: un nuovo progetto deve essere aggiunto al sistema.
* **POST**: il sistema comunica all’utilizzatore l’errore e il progetto non viene inserito.
* **Estensioni**: -

### UC18.3 Errore URL non raggiungibile

* **Titolo**: Errore URL non raggiungibile.
* **Attori primari**: utente.
* **Descrizione**: l’utente viene avvisato che il progetto che vorrebbe aggiungere non è raggiungibile (i.e. non esiste). 
* **PRE**: un nuovo progetto deve essere aggiunto al sistema.
* **POST**: il sistema comunica all’utilizzatore l’errore e il progetto non viene inserito.
* **Estensioni**: -

### UC19 Rimozione Progetto
-->
## Alternative

Creare un caso d'uso per ogni coppia Producer-Consumer
* Problema: complessità esponenziale

## Sottosistemi

* Producer Redmine
* Producer Gitlab
* Gestore Personale
* Coda Telegram
* Coda email

## GitLab Issue Event

* `obj["object_kind"]`
* `obj["project"]["id"]/obj["object_attributes"]["project_id"]`
* `obj["project"]["name"]`
* `obj["assignees"][k]["nome utente"]`
* `obj["object_attributes"]["action"]` (se ="close", da scartare)
* `obj["object_attributes"]["description"]`
* `obj["labels"][k]["title"]`
* `obj["labels"][k]["project_id"]`
* `obj["changes"]["title"]`
* `obj["changes"]["labels"]["previous"][k]["title"]`
* `obj["changes"]["labels"]["current"][k]["title"]`

## GitLab Push Event

* `obj["object_kind"] = "push"`
* `obj["utente_id"]`
* `obj["utente_nome utente"]`
* `obj["project_id"]`
* `obj["commits"][k]["id"]`
* `obj["commits"][k]["message"]`
* `obj["commits"][k]["timestamp"]`
* `obj["commits"][k]["author"]["name"]`
* `obj["total_commits_count"]`

## Redmine Issue Event
(Plugin: https://github.com/suer/redmine_webhook)

* `obj["payload"]["issue"]["priority"]["name"]`
* `obj["payload"]["issue"]["tracker"]["name"]`
* `obj["payload"]["issue"]["subject"]`
* `obj["payload"]["issue"]["status"]["name"]`
* `obj["payload"]["issue"]["description"]`
* `obj["payload"]["issue"]["project"]["id"]`
* `obj["payload"]["issue"]["project"]["name"]`
* `obj["payload"]["issue"]["action"]`

### Da aggiungere in AdR

* Aggiungere un **include** al caso d'uso 15.1 dove l'utente **esce dall'applicazione**?

* Aggiungere caso d'uso dove il **Gestore Personale** guarda se una persona è disponibile e dunque fare l'inoltro (tra il 7 e l'8)

* Dire che l'identificativo è conposto dalla mail o dall'ID Telegram, peciò uno dei due è necessario

* Pensare ad una figura a cui inoltrare i messaggi in caso di inoltro infinito (**amministratore**)

* Pensare ad una figura già iscritta nel sistema che inizialmente possa aggiungere tutti gli altri utenti (**amministratore**)

* Scrivere **tutto** in §2

* Capire meglio il contesto del termine **registrazione**

* La registrazione deve poter essere fatta fuori dal sistema (perciò l'utente pre registrato non c'è più)