### ConsoleProducer

Prima di lanciare un Producer, dovresti configurare l'[ambiente Kafka](https://github.com/Vashy/AlphaSix/tree/develop/Butterfly/README.md) ed
eventualmente un [Consumer](https://github.com/Vashy/AlphaSix/tree/develop/Butterfly/consumer/README.md).

Per mandare uno o più messaggi da linea di comando su Kafka in un topic specifico, posizionarsi nella cartella `Butterfly/` e dare il comando:

    $ python3 -m producer.ConsoleProducer -t nometopic msg1 msg2 "messaggio numero 3" ...

Nell'esempio sopra, verranno passati su Kafka 3 messaggi, tutti al topic *nometopic*. Usare preferibilmente i topic `enhancement`, `bug` o `wontfix`, che sono i 3 definiti nel json
di configurazione dei Consumer.

I messaggi mandati sono:
* msg1
* msg2
* messaggio numero 3

È possibile passare un numero arbitrario di argomenti, per ognuno di essi verrà generato su Kafka un messaggio diverso sul Topic specificato.

La flag `-t` è opzionale, se omessa verrà usato un topic di default.


### GLProducer

Per mandare un messaggio come Webhook di GitLab (attualmente il file `webhook.json` contenuto in `webhook/`), dare il comando

    $ python3 -m producer.gitlab.GLProducer -t nometopic

La flag `-t` è opzionale, se omessa verrà usato un topic di default.

### RedmineProducer

Per mandare un messaggio come Webhook di Redmine (attualmente il file `open_issue_redmine_webhook.json`), dare il comando

    $ python3 -m producer.redmine.RedmineProducer -t nometopic

La flag `-t` è opzionale, se omessa verrà usato un topic di default.
