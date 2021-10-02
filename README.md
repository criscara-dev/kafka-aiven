# Aiven Homework

As part of the demo application you must be able to send events to a Kafka topic (a producer) which will then be read by a Kafka consumer application that you've written. 
The consumer application must then store the consumed data to an Aiven PostgreSQL database.

In short: Utilise Aiven's Postgres and Kafka services to produce data as an event into a Kafka topic and consume into a Postgres database.

---

### How to run the app

To launch this solution you will need:


Launch main.py which will call consumer and producer.
This way the Consumer is up and running when the Producer send the messages.


1. Signup to Aiven.io and Create managed instances of Apache Kafka and PostgreSQL.
3. Be sure to install Python modules as from requirements.txt
4. Produce and read Messages to Apache Kafka:
   1. for simplicity I have created a main file that you can run and have your Producer and Consumer working without run 2 separate files:
      Run main.py that will call two functions; one for consumer and one for producer files.
      (since Kafka Consumer start to read since the time that is attached to kafka, I am running this first and after the producer with some delay)
   2. Consumer is receiving correctly [events and schema](./img/aiven-topic-events.png).
5. In Aiven.io create a _[JDBC Sink](https://github.com/aiven/aiven-kafka-connect-jdbc/blob/master/docs/sink-connector.md)_, i.e. a single config file.
   This Kafka Connector is a prebuilt framework enabling an easy integration of Apache Kafka with existing data sources or sinks;  
6. Open your preferred management tool for PostgreSQL ( for me with PGAdmin ), and add connections parameters (if you don't know how, please follow [these steps](https://developer.aiven.io/docs/products/postgresql/howto/connect-pgadmin.html).
7. If everything has worked out for you should have a _table_ populated with the data coming from the **kafka connector**.

---

### Testing - Implementation / Complete the Project

- Testing the Python code
- Produce data for tests
- I couldn't complete the task* and I then couldn't do some testing;
  Imagining that the data in the PostgreSQL DB was consumed by a web app, I could have tested the availability of the service, for example using libraries such as _BeautifulSoup_ and _requests_ 
- I struggled to configure the connector (JSON file) in a way that was performing properly and, I was constantly receiving an error;
  I open a ticket with the Support team, but we couldn't resolve the case. They let me know that some article's information (about create the JSON for the configuration) needs some updates. 

- The final result I was expecting what using kafka connect to create the table, populate the table and keep populate the table in PostgreSQL DB as soon as new data was arrived to the kafka topic.
This may not be possible because even if the connector [was starting fine](./img/connector-start-ok.png), soon an error appear [connector](./img/connector-error.png).
The [database](./img/pgadmin.png) was connecting but no table was created.

---

### Tools
GUI tool used to interact with the Postgres database sessions: [PGAdmin](https://www.pgadmin.org/)

IDE: [PyCharm](https://www.jetbrains.com/pycharm/)

To manages open source data infrastructure in the cloud: [Aiven.io](https://aiven.io/)

---

### Resources/References

Tutorial: [Event-driven applications: Apache Kafka and Python | Francesco Tisiot | Conf42 Python 2021](https://www.youtube.com/watch?v=LCXyBzHEqFM)

---

### GitHub repo:

[Aiven kafka-python-notebooks](https://github.com/aiven/kafka-python-notebooks/blob/main/00%20-%20Aiven%20Setup.ipynb)

---

### Aiven articles:

[An introduction to PostgreSQL](https://aiven.io/blog/an-introduction-to-postgresql)

[getting-started-with-aiven-for-apache-kafka](https://help.aiven.io/en/articles/489572-getting-started-with-aiven-for-apache-kafka)

[setting-up-a-jdbc-sink-connector-with-aiven-for-apache-kafka](https://help.aiven.io/en/articles/4278191-setting-up-a-jdbc-sink-connector-with-aiven-for-apache-kafka)

[JDBC source connector with PostgreSQL](https://help.aiven.io/en/articles/3416789-jdbc-source-connector-with-postgresql)

[Connect with Python](https://developer.aiven.io/docs/products/postgresql/howto/connect-python.html)

[Connect with pgAdmin](https://developer.aiven.io/docs/products/postgresql/howto/connect-pgadmin.html)

[Error Reporting in Connect](https://kafka.apache.org/documentation/#:~:text=error%20reporting%20in%20connect)

[postgresql](https://developer.aiven.io/docs/products/postgresql/getting-started.html)

Postgres Tutorial:

[Connect To PostgreSQL Database Server](https://www.postgresqltutorial.com/postgresql-python/connect/)


---

## License

This project is licensed under the [Apache License Version 2.0](./LICENSE).