# This script connects to Kafka and send a few messages

from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import os
from faker import Faker


# PG_USER_PASS = os.environ['PG_PASS']
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")


def producer_run():
    try:
        folderName = "kafkaCerts/"

        producer = KafkaProducer(
            bootstrap_servers=SERVER_URL,
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

        # send fake data to test service; in real scenario data won't be hardcoded
        fake = Faker()
        name = fake.name()
        address = fake.address()
        phone_number = fake.phone_number()
        unique_id = fake.iana_id()

        producer.send(
            "jdbc_sink" + "_schema",
            key={"schema": key_schema, "payload": {"id": unique_id}},
            value={"schema": value_schema,
                   "payload": {"name": name, "address": address, "telephone": phone_number}}
        )

        # Force sending of all messages
        producer.flush()

        result = True
    except KafkaError as e:
        print(f"Exception during publishing messages - {e}.")
        result = False

    return result


producer_run()
