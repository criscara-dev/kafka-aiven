# This script receives messages from a Kafka topic

from kafka import KafkaConsumer
import json
import psycopg2
from kafka.errors import KafkaError
import os


# PG_USER_PASS = os.environ['PG_PASS']
from dotenv import load_dotenv

load_dotenv()

PG_SUPER_PASS = os.getenv("PG_SUPER_PASS")
SERVER_URL = os.getenv("SERVER_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
GROUP_ID = os.getenv("GROUP_ID")

PG_DBNAME = os.getenv("PG_DBNAME")
PG_SUPER_USER = os.getenv("PG_SUPER_USER")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")

def consumer_run():
    try:
        folder_name = "kafkaCerts/"

        consumer = KafkaConsumer(
            "jdbc_sink",
            auto_offset_reset="earliest",
            bootstrap_servers=SERVER_URL,
            client_id=CLIENT_ID,
            group_id=GROUP_ID,
            security_protocol="SSL",
            ssl_cafile=folder_name + "ca.pem",
            ssl_certfile=folder_name + "service.cert",
            ssl_keyfile=folder_name + "service.key",
            value_deserializer=lambda v: json.loads(v.decode('ascii')),
            key_deserializer=lambda v: json.loads(v.decode('ascii')),
            max_poll_records=10
        )

        """ Connect to the PostgreSQL database server """
        conn = None
        try:

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')

            conn = psycopg2.connect(dbname=PG_DBNAME,
                                    user=PG_SUPER_USER,
                                    host=PG_HOST,
                                    port=PG_PORT,
                                    password=PG_SUPER_PASS,
                                    sslmode='require')

            # create a cursor
            cur = conn.cursor()
            cur.execute("GRANT CONNECT ON DATABASE defaultdb TO " + PG_USER + ";")
            cur.execute("GRANT USAGE ON SCHEMA public TO " + PG_USER + ";")

            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

        consumer.topics()
        consumer.subscribe(topics=["jdbc_sink_schema"])
        consumer.subscription()

        for message in consumer:
            print("%d:%d: k=%s v=%s" % (message.partition,
                                        message.offset,
                                        message.key,
                                        message.value))

        # Commit offsets so we won't get the same messages again
        consumer.commit()
        consumer.close()

    except KafkaError as exc:
        print(f"Kafka consumer - Exception during connecting to broker - {e}.")
