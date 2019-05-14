# Consumer

Il Consumer è il componente finale del sistema Butterfly. Esso resta in ascolto della sua coda specifica di Kafka per applicativo (e.g. telegram, email). Si occupa di inoltrare il messaggio al destinatario finale.

Prima di lanciare un Consumer bisogna configurare l'ambiente di [Butterfly](https://github.com/Vashy/AlphaSix/blob/master/README.md).

## Consumer Email

Il Consumer Email si occupa di prelevare i messaggi all'interno della coda "email" in Kafka ed inoltrarli ai destinatari appropriati in base all'indirizzo email indicato dal destinatario. La mail viene inviata dall'account specificato nei file di [configurazione](https://github.com/Vashy/AlphaSix/blob/master/Butterfly/consumer/config.json).

## Consumer Telegram

Il Consumer Telegram si occupa di prelevare i messaggi all'interno della coda "telegram" in Kafka ed inoltrarli ai destinatari appropriati in base all'ID Telegram dei destinatati.

Per individurare il proprio ID Telegram è consigliato usare [MyIDBot](tg://resolve?domain=storebot&start=myidbot) ed eseguire il comando `/getid`. 