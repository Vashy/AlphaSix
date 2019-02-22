# Avviare il servizio mongod

È necessario avere `mongodb` installato correttamente nel sistema.

Dare il comando:

    $ sudo service mongod start

per avviare il demone di MongoDB.

# Popolare il Database

Dalla cartella `Butterfly/`, dare il comando:

    $ python3 -m mongo_db.populate

per popolare il database, attraverso il file `db.json`
