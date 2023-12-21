#!/usr/bin/env python

import pulsar
import time

time.sleep(10)
print("Connecting to Pulsar broker...")
client = pulsar.Client('pulsar://127.0.0.1:6650')
print("Connected to broker!")

print("Creating producer...")
producer = client.create_producer('persistent://public/default/my-topic')
print(producer.is_connected())

for i in range(10):
    try:
        producer.send(('hello-pulsar-%d' % i).encode('utf-8'))
        print(f"Message sent: hello-pulsar-{i}")
    except pulsar.PulsarException as e:
        print(f"Error sending message: {e}")

    time.sleep(2)  # Give some time for messages to be sent

client.close()
