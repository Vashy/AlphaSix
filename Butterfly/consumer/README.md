# Lanciare il Consumer Telegram

Prima di lanciare un Consumer, dovresti configurare l'[ambiente Kafka](https://github.com/Vashy/AlphaSix/blob/b6f3a176088e3b822261c5f0381d26017d351463/Butterfly/README.md).

Il TelegramConsumer si mette in ascolto dei Topic verso cui è configurato in `config.json` (li creerà direttamente su Kafka in caso non siano presenti),
e li inoltra all'utente Telegram con l'ID definita nello stesso file.

Posizionarsi in `Butterfly/` e lanciare il comando

    $ python3 -m consumer.telegram.TelegramConsumer

Lasciare il processo in esecuzione per ascoltare e inoltrare i vari messaggi.
