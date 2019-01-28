### Starting Kafka Server
Position: Kafka home dir (e.g. `~/Desktop/kafka_2.11-2.1.0`)
> `bin/kafka-server-start.sh config/server.properties`

### Create Topics
Position: Kafka home dir
> `bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test`

### List all available topics
Position: Kafka home dir
> `bin/kafka-topics.sh --list --zookeeper localhost:2181`

### Run the Consumer
Position: Kafka home dir
> `bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test`  

### Run the Consumer, list messages from beginning
Position: Kafka home dir
> `bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning`  

### Run the Python script
Posizione: `.../AlphaSix/`
> `python3 Butterfly/butterfly/producer.py msg1 msg2 ... msgK`  
(K >= 0)
