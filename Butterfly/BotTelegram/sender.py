import telepot
import time


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        print('ID utente: ', chat_id)
        name = msg["from"]["first_name"]
        print('Nome utente: ', name)
        text = msg['text']
        print('Testo messaggio: ', text)
        print('-----------')
        if text == '/start':
            bot.sendMessage(chat_id, 'Ciao {}, questo è il bot che ti invierà le segnalazioni dei topic ai quali ti sei iscritto.'.format(name))
        else:
            bot.sendMessage(chat_id, 'Non inviarmi messaggi, sono impegnato e non ho tempo per risponderti.')


# il token è l'ID univoco del bot che deve rimanere segreto, altrimenti chiunque può metterci le mani.
token = '767404683:AAF6Fo4LP7wDWYmEbIRQ37KTX5GECMoTziA'
bot = telepot.Bot(token)


def main():
    # viene chiamata ogni volta che il bot riceve un messaggio
    bot.message_loop(on_chat_message)

    print('Listening ...')

    # procede all'infinito a intervalli di un secondo
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
