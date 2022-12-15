# On the consumer’s side, you’ll be able to read the sent messages by iterating over the consumer
# The consumer’s constructor takes one or more topics that it might be interested in

from kafka3 import KafkaConsumer

consumer = KafkaConsumer("datascience")
for record in consumer:
    message = record.value.decode("utf-8")
    print(f"Got message: {message}")