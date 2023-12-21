#!/usr/bin/env python

import pulsar
import time

time.sleep(5)

client = pulsar.Client('pulsar://127.0.0.1:6650')
consumer = client.subscribe('my-topic', subscription_name='my-sub')

while True:
    msg = consumer.receive()
    print("Received message: '%s'" % msg.data())
    consumer.acknowledge(msg)

client.close()
