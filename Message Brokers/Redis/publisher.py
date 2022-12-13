# Redis is short for Remote Dictionary Server
# It’s an in-memory key-value data store that usually works as an ultra-fast cache between a traditional SQL database and a server
# At the same time, it can serve as a persistent NoSQL database and also a message broker in the publish-subscribe model

import redis

with redis.Redis() as client:
    while True:
        message = input("Message: ")
        client.publish("chatroom", message)