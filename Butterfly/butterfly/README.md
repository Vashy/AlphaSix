### Starting Zookeeper
Posizione: Kafka home dir (e.g. `path/to/kafka_2.11-2.1.0/`)
> `bin/zookeeper-server-start.sh config/zookeeper.properties`

### Starting Kafka Server
Posizione: Kafka home dir (`path/to/kafka_2.11-2.1.0/`)
> `bin/kafka-server-start.sh config/server.properties`

### Create Topics
Posizione: Kafka home dir
> `bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test`

### List all available topics
Posizione: Kafka home dir
> `bin/kafka-topics.sh --list --zookeeper localhost:2181`

### Run the Consumer
Posizione: Kafka home dir
> `bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test` 

## Python scripts

Precondizione: è necessario avere il pacchetto `kafka-python` installato nel sistema.
> `pip3 install kafka-python`

### Run the Python Consumer

> `path/to/consumer.py`

(si mette in ascolto di tutti i topic definiti nel file `topics.json`)


<!-- ### Run the Consumer
Posizione: Kafka home dir
> `bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test`   -->

<!-- ### Run the Consumer, list messages from beginning
Posizione: Kafka home dir
> `bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning`   -->

### Run the Python Producer

> `python3 path/to/producer.py -t nometopic msg1 msg2 ... msgK`  
(K >= 0)
