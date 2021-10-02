# This script connects to Kafka and send a few messages

from kafka import KafkaProducer
from kafka.errors import KafkaError
import json


def producer_run():
    try:
        folderName = "kafkaCerts/"

        producer = KafkaProducer(
            bootstrap_servers="kafka-1553967d-project-b54b.aivencloud.com:22903",
            security_protocol="SSL",
            ssl_cafile=folderName + "ca.pem",
            ssl_certfile=folderName + "service.cert",
            ssl_keyfile=folderName + "service.key",
            value_serializer=lambda v: json.dumps(v).encode('ascii'),
            key_serializer=lambda v: json.dumps(v).encode('ascii')
        )

        key_schema = {
            "type": "struct",
            "fields": [
                {
                    "type": "int32",
                    "optional": False,
                    "field": "id"
                }
            ]
        }

        value_schema = {
            "type": "struct",
            "fields": [
                {
                    "type": "string",
                    "optional": False,
                    "field": "name"
                },
                {
                    "type": "string",
                    "optional": False,
                    "field": "address"},
                {
                    "type": "int",
                    "optional": False,
                    "field": "telephone"}
            ]
        }

        producer.send(
            "jdbc_sink" + "_schema",
            key={"schema": key_schema, "payload": {"id": 1}},
            value={"schema": value_schema,
                   "payload": {"name": "John Watson", "address": "Baker Street, 221", "telephone": "0737846583"}}
        )

        producer.send(
            "jdbc_sink" + "_schema",
            key={"schema": key_schema, "payload": {"id": 2}},
            value={"schema": value_schema,
                   "payload": {"name": "Sherlock Holmes", "address": "Baker Street, 221", "telephone": "0737846583"}}
        )

        # Force sending of all messages
        producer.flush()

        result = True
    except KafkaError as e:
        print(f"Exception during publishing messages - {e}.")
        result = False

    return result


producer_run()
