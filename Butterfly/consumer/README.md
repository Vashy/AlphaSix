# Lanciare il Consumer Telegram

Prima di lanciare un Consumer, dovresti configurare l'ambiente Kafka.

Il TelegramConsumer si mette in ascolto dei Topic verso cui è configurato in `config.json`, e li inoltra all'utente Telegram con l'ID definita nello stesso file.

Posizionarsi in `Butterfly` e lanciare il comando

    $ python3 -m consumer.telegram.TelegramConsumer

Lasciare il processo in esecuzione per ascoltare e inoltrare i vari messaggi.
