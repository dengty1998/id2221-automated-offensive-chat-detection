from confluent_kafka import Producer


def kafka_producer():

    producer_config = {
        'bootstrap.servers': 'localhost:9092'
    }
    producer = Producer(producer_config)
    return producer


def flush_message(topic, value):

    producer_connection = kafka_producer()
    producer_connection.produce(topic, value=value)
    producer_connection.flush()