# Producer can send messages on a given topic

from kafka3 import KafkaProducer

producer = KafkaProducer(bootstrap_servers="localhost:9092")
while True:
    # The .send() method is asynchronous because it returns a future object that you can await by calling its blocking .get() method
    message = input("Message: ")
    producer.send(
        topic="datascience",
        value=message.encode("utf-8"),
    )