﻿# 4411-apache-pulsar

If you'd like to check out the video this guide is based upon --> https://youtu.be/w2dzxQfAiZM?list=PL7-BmxsE3q4Vzhzqlx128ixxRQMeKOa6C

## Setting up Docker and the Pulsar Cluster
Run the image in Docker:
```bash
docker run -it -p 6650:6650 -p 8080:8080 --name pulsar --mount source=pulsardata,target=/pulsar/data --mount source=pulsarconf,target=/pulsar/conf apachepulsar/pulsar:3.1.1 bin/pulsar standalone
```
Note: This creates 1 Zookkeeper instance, 1 Bookeeper instance, and 1 Broker instance. The name of our Docker image is `pulsar` and the cluster name is `standalone`.


Get into the Docker terminal for the image:
```bash
docker exec -it pulsar /bin/bash
```

List the available clusters:
```bash
bin/pulsar-admin clusters list
```

Get info for a specific cluster:
```bash
bin/pulsar-admin clusters get standalone
```

List the existing tenants (this should return nothing as we haven't yet created a tenant):
```bash
bin/pulsar-admin clusters tenants list
```

Note: Remember that Apache Pulsar is a multi-tenant system, so the topic URL structure we want looks like this:
*`persistent*://tenant/namespace/topic` 

### Now, let's create our tenant, namespace, and topic!
Create a tenant:
```bash
bin/pulsar-admin tenants create --admin-roles admin --allowed-clusters standalone investments
```

Get tenant information (to verify it was created successfully):
```bash
bin/pulsar-admin tenants get [tenant_name]
```

Create a namespace (Note that `investments` is the tenant we just previously created)
```bash
bin/pulsar-admin namespaces create investments/stocks
```

Create a topic:
```bash
bin/pulsar-admin topics create persistent://investments/stocks/stocks-ticker
```
Note: The use of persistent here - this is the default for tenants. If our tenant was non-persistent, data would not be kept inside the Broker cache so if message sending fails or the Broker crashes, we would lose all data. However non-persistent topics benefit from better performance and throughput. 

## Communicating between Producer -> Consumer
In a new terminal, execute the following:
```bash
docker exec -it pulsar /bin/bash
bin/pulsar-client consume -s "test-subs" -p Earliest -n 0 stock-tickers
```
Note: We are starting up a Pulsar consumer here called `test-subs`. The flags `-n 0` mean that it will consuming from the earliest unconsumed message; `-n` configures the number of messages to consume, `0` means to consume forever.

Go back to the other Docker terminal we had open, or open another one so we can write some messages to our `stock-tickers` topic.
```bash
bin/pulsar-client produce stock-tickers --messages 'Hello Pulsar!'
```
After running the producer command, you should see `[main] INFO  org.apache.pulsar.client.cli.PulsarClientTool - 1 messages successfully produced`. Go back to the terminal with the consumer and you should see `----- got message -----
key:[null], properties:[], content:Hello Pulsar!` if everything is working correctly. 



## Admin API
Some admin api commands that will be useful when we do analysis of different Pulsar features and their efficiency/performance.

Get a lot of great statistics about the topic, such as msgRateOut/In, msgThroughputOut, backlogSize. We can also run similar commands for the Producer, Consumer, Subscription etc.
```bash
bin/pulsar-admin topics stats persistent://investments/stocks/stock-tickers'
```

Get internal stats about the 10 most recent messages:
```bash
bin/pulsar-admin topics peek-messages --count 10 --subscription my-subscription persistent://test-tenant/ns1/tp1
```
