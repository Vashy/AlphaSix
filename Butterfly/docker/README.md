#  Configurazione del sistema Butterfly

Viene fornito un file ```docker-compose.yml``` che contiene la configurazione per il sistema e per i servizi che vengono utilizzati dalla nostra applicazione.
Per eseguirlo è necessario avere almeno la versione XX.XX.XX di Docker installata nel sistema.

I file di log che vengono utilizzati sono formato json-file 
Prima di eseguire fare configurazione per file log

Mandare il comando all'interno della cartella in cui è presente il file:
 
 	$ docker-compose up -d ; 
 
L'opzione ```-d``` serve per effettuare il ```detach```, ovvero il processo viene eseguito headless / daemon.
 
I servizi verranno configurati in questo ordine e saranno accessibili tramite i seguenti link con porte ...
 
* **Jenkins** : 
Le porte esposte per Jenkins sono:  1500:8080
Per configurare il servizio Jenkins andare all'indirizzo localhost:1500
La password che viene richiesta si può trovare nel container nel file ...
Per ulteriori informazioni non presenti riferirsi alla [documentazione ufficiale](https://github.com/jenkinsci/docker/blob/master/README.md).

* **Gitlab** :
Il servizio GitLab mette a disposizione le porte 
    - *1501:80* per la connessione all'interfaccia web tramite http
    - *1502:443* per la connessione all'interfaccia web tramite https
    - *1503:22* per la connessione tramite ssh al container
    
	Per la prima autenticazione utilizzare ... E' possibile accedere al servizio tramite le credenziali admin admin che verrà subito chiesto di essere cambiate.
Per ulteriori informazioni non presenti riferirsi alla [documentazione ufficiale](https://docs.gitlab.com/omnibus/docker/).

* **Postgres** :
* **Redmine** :
All'interno della cartella docker/plugins/redmine è presente il plugin ... di redmine per i webhook
Per ulteriori informazioni non presenti riferirsi alla [documentazione ufficiale](https://github.com/suer/redmine_webhook).

* **Producer Gitlab** :

* **Consumer Telegram** :
Serve per le interazioni con il bot di telegram online che si chiama ... 
Il consumer Telegram fatto da noi da la possibilità di bla ..
E' possibile vedere i log dei messaggi inviati

* **Apache kafka** :
 
 
 
Per ciascun container, i file di log sono disponibili nella cartella  ```/var/lib/docker/containers/ID_CONTAINER``` e sono di tipo ```*-json.log```.
	
	$ docker inspect --format='{{.LogPath}}' NOME_CONTAINER / ID_CONTAINER ; 
	
	/var/lib/docker/containers/[container-id]/[container-id]-json.log
	
Per facilitare la gestione dei container è possibile utilizzare un programma free di terze parti chiamato dockerhost