# Lanciare il Consumer Telegram

Prima di lanciare un Consumer, dovresti configurare l'[ambiente Kafka](https://github.com/Vashy/AlphaSix/tree/develop/Butterfly/README.md).

Il TelegramConsumer si mette in ascolto dei Topic verso cui è configurato in `config.json` (li creerà direttamente su Kafka in caso non siano presenti),
e li inoltra all'utente Telegram con l'ID definita nello stesso file.

Posizionarsi in `Butterfly/` e lanciare il comando

    $ python3 -m consumer.telegram.TelegramConsumer

Lasciare il processo in esecuzione per ascoltare e inoltrare i vari messaggi.

# Lanciare il Consumer Email

Prima di lanciare un Consumer, dovresti configurare l'[ambiente Kafka](https://github.com/Vashy/AlphaSix/tree/develop/Butterfly/README.md).

L'EmailConsumer si mette in ascolto dei Topic verso cui è configurato in `config.json` (li creerà direttamente su Kafka in caso non siano presenti),
e li inoltra all'email con l'ID definita nello stesso file.

Posizionarsi in `Butterfly/` e lanciare il comando

    $ python3 -m consumer.email.EmailConsumer

Lasciare il processo in esecuzione per ascoltare e inoltrare i vari messaggi.
