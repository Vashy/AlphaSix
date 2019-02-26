#!/usr/bin/env python3

# Uso: python3 path/to/prova.py 'messaggio da inviare'
# Dando chmod+x sullo script è possibile omettere python3

import smtplib, argparse

parser = argparse.ArgumentParser(description='Form di invio email')
parser.add_argument('-r', dest='receiver', type=str, nargs='+',
                    help='Email destinatario: ')
parser.add_argument('-s', dest='subject', type=str, nargs='+',
                    help='Soggetto dell\'email: ')
parser.add_argument('-b', dest='body', type=str, nargs='+',
                    help='Testo dell\'email: ')

args = parser.parse_args()

sender = 'alpha.six.unipd@gmail.com'
pwd = 'alfa6swe'
mailserver = smtplib.SMTP('smtp.gmail.com', 587)
mailserver.ehlo()
mailserver.starttls()
mailserver.login(sender, pwd)

text = '\r\n'.join([
  'From: '+sender,
  'To: '+' '.join(args.receiver),
  'Subject: '+' '.join(args.subject),
  '',
  ' '.join(args.body)
  ])

mailserver.sendmail(sender, ' '.join(args.receiver), text)
mailserver.close()

print('Email inviata')