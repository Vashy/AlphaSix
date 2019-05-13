# Gestore Personale

**Gestore Personale** è la componente del sistema **Butterfly** usata per la gestione dei dati relativi a **utenti** e **progetti**. Per svolgere il suo scopo tale componente è stata suddivisa in due sottocomponenti, **client** e **controller**, rispettivamente per la gestione delle interazioni con le code di kafka e con l'utente.

## Client
Questa sottocomponente del Gestore Personale è configurata in modo da rimanere in ascolto sulle code di kafka in output dai **producer redmine** e **gitlab**. Quando arriva un messaggio relativo a una issue o a un commit, esso viene scomposto e confrontato con i dati salvati sul database **Mongo** relativi ai progetti.
In caso il progetto non esista, esso viene automaticamente salvato. In caso contrario il messaggio viene inoltrato agli utenti interessati a seconda della priorità di progetto impostata e delle preferenze impostate attraverso il **controller**.

## Controller
Questa sottocomponente resta in ascolto attraverso un server HTTP delle richieste degli utenti, che possono modificare i propri dati e le proprie preferenze relative ai progetti, ai giorni di irreperibilità e alla piattaforma di messaggistica preferita.
Gli utenti amministratori possono inoltre aggiungere altri utenti, rimuovere progetti e preferenze associate e visualizzare nel dettaglio tutti i dati relativi a utenti e progetti esistenti.

### Web
Questa sottocomponente del controller viene usata per gestire le richieste provenienti da un client Web. Viene usata attraverso l'interfaccia Web.

### Api
Questa sottocomponente del controller viene usata per gestire le richieste provenienti da un client HTTP qualsiasi con supporto al formato JSON.
Le richieste effettuate devono rispettare lo stile architetturale REST secondo le regole illustrate nel Manuale Utente.


# Popolare il database o reset
Prima di popolare il database, dovresti lanciare [mongo](https://github.com/Vashy/AlphaSix/tree/develop/Butterfly/mongo_db/README.md)
Per popolare il database al primo avvio, posizionarsi in `Butterfly/` e dare il comando

    $ python3 -m mongo_db.populate

Tale comando popola il database con l'utente amministratore e i suoi dati presenti nel file `config.json` presenti nella cartella `Butterfly/mongo_db/`.

# Avviare il controller
Per avviare il controller, posizionarsi in `Butterfly/` e dare il comando

    $ python3 -m gestore_personale.controller

Tale comando inizializza il server HTTP Flask, che resta in ascolto delle richieste dei client.

Per vedere l'installazione e la configurazione che è stata effettuata per la proponente vi rimandiamo ai documenti Manuale Utente e Manuale Sviluppatore rilasciati insieme al prodptto.
