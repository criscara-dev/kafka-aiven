# This script receives messages from a Kafka topic

from kafka import KafkaConsumer
import json
import psycopg2
from kafka.errors import KafkaError
import os


# PG_USER_PASS = os.environ['PG_PASS']
from dotenv import load_dotenv

load_dotenv()

PG_USER_PASS = os.getenv("PG_USER_PASS")

def consumer_run():
    try:
        folder_name = "kafkaCerts/"

        consumer = KafkaConsumer(
            "jdbc_sink",
            auto_offset_reset="earliest",
            bootstrap_servers="kafka-1553967d-project-b54b.aivencloud.com:22903",
            client_id="demo-client-1",
            group_id="demo-group",
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
            pg_dbname = "defaultdb"
            pg_super_user = "avnadmin"
            pg_host = "pg-31f5faa7-project-b54b.aivencloud.com"
            pg_port = 22901
            pg_super_pwd = PG_USER_PASS
            pg_user = "avnadmin"

            conn = psycopg2.connect(dbname=pg_dbname,
                                    user=pg_super_user,
                                    host=pg_host,
                                    port=pg_port,
                                    password=pg_super_pwd,
                                    sslmode='require')

            # create a cursor
            cur = conn.cursor()
            cur.execute("GRANT CONNECT ON DATABASE defaultdb TO " + pg_user + ";")
            cur.execute("GRANT USAGE ON SCHEMA public TO " + pg_user + ";")

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
