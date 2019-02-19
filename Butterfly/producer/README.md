### ConsoleProducer

Prima di lanciare un Producer, dovresti configurare l'ambiente Kafka ed eventualmente un Consumer.

Per mandare uno o più messaggi da linea di comando su Kafka in un topic specifico, posizionarsi nella cartella `Butterfly/` e dare il comando:

    $ python3 -m producer.ConsoleProducer -t nometopic msg1 msg2 "messaggio numero 3"

Verranno passati su Kafka 3 messaggi, tutti al topic *nometopic*. Usare preferibilmente i topic `enhancement`, `bug` o `wontfix`, che sono i 3 definiti nel json
di configurazione dei Consumer.

I messaggi mandati sono:
* msg1
* msg2
* messaggio numero 3

Per mandare un messaggio come Webhook di GitLab (attualmente il file `webhook.json` contenuto in `webhook/`), dare il comando

    $ python3 -m producer.GLProducer -t nometopic

La flag `-t` è opzionale per entrambi i comandi, se omessa verrà usato un topic di default.