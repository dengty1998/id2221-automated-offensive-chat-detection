from confluent_kafka import Consumer, KafkaError
from Connectors.hdfs_connector import append_json
from Connectors.redis_connector import push_json

def kafka_consumer():
    consumer_config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'my-consumer-group',
        'auto.offset.reset': 'earliest'  # Start consuming from the beginning of the topic.
    }

    # Create a Kafka consumer instance
    consumer = Consumer(consumer_config)

    return consumer


def consume_message(topic):
# Subscribe to a topic

    consumer = kafka_consumer()
    consumer.subscribe([topic])

    # Start consuming messages
    while True:
        msg = consumer.poll(1.0)  # Poll for messages, with a timeout (1 second in this case)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('Reached end of partition')
            else:
                print(f'Error while consuming: {msg.error()}')
        else:
            # json_text = {
            #     'username': str(message['username']),
            #     'message': str(message['msg']),
            #     'timestamp': str(timestamp),
            # }
            message = msg.value().decode('utf-8')

            push_json("chatlogs", message)
            append_json("/chatlogs/chatlogs.json", message)
            print(f'Received message: value={message}')

    # Close the consumer when done
    consumer.close()


