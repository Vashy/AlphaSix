# Avviare il servizio mongod

È necessario avere `mongodb` installato correttamente nel sistema.

Dare il comando:

    $ sudo service mongod start

per avviare il demone di MongoDB.

# Popolare il Database

Dalla cartella `Butterfly/`, dare il comando:

    $ python3 -m mongo_db.populate

per popolare il database, attraverso il file `db.json`

# Lanciare i test

Dalla cartella `Butterfly/` dare il comando:

    $ python3 -m mongo_db.tests.db_controller_test

A ogni esecuzione dei test *è necessario* ripopolare il Database (vedi la sezione sopra).
