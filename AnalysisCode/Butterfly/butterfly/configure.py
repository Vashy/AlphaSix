#!/usr/bin/env python3
import subprocess, argparse
from pathlib import Path

parser = argparse.ArgumentParser("Initialize kafka environment")

parser.add_argument(
    '-t', '--topics',
    nargs='*',
    action='store',
    help='Lista di Topic da inizializzare'
)

parser.add_argument(
    '-p', '--path',
    nargs=1,
    type=str,
    required=True,
    help='Path alla home directory di Kafka'
)

parser.add_argument(
    '-z', '--zookeeper',
    action='store_true',
    help='Flag che segnala se avviare il server Zookeeper'
)

parser.add_argument(
    '-k', '--kafka',
    action='store_true',
    help='Flag che segnala se avviare il server Kafka'
)

args = parser.parse_args()
args.path = args.path[0]

if args.zookeeper:
    zookeeper_server = "bin/zookeeper-server-start.sh"
    zookeeper_config = "config/zookeeper.properties"
    
    zookeeper_path = Path(args.path) / zookeeper_server
    zookeeper_config_path = Path(args.path) / zookeeper_config
    # print(zookeeper_path, zookeeper_config_path)
    subprocess.Popen(('{} {}'.format(zookeeper_path, zookeeper_config_path)).split())

if args.kafka:
    # bin/kafka-server-start.sh config/server.properties
    kafka_server = "bin/kafka-server-start.sh"
    kafka_config = "config/server.properties"

    kafka_path = Path(args.path) / kafka_server
    kafka_config_path = Path(args.path) / kafka_config
    # print(kafka_path, kafka_config_path)
    subprocess.Popen('{} {}'.format(kafka_path, kafka_config_path).split())

DEFAULT_TOPICS = [
    "wontfix",
    "bug",
    "enhancement"
]

# if len(args.topics) == 0:
#     pass
