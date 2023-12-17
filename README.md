# 4411-apache-pulsar

## Setting up Docker and the Cluster
Run the image in Docker:
```bash
docker run -it -p 6650:6650 -p 8080:8080 --name pulsar --mount source=pulsardata,target=/pulsar/data --mount source=pulsarconf,target=/pulsar/conf apachepulsar/pulsar:3.1.1 bin/pulsar standalone
```
Note: This creates 1 zookkeeper instance, 1 bookeeper instance, and 1 broker instance. The name of our Docker image is `pulsar` and the cluster name is `standalone`.


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

### Now let's create our tenant, namespace, and topic.
Create a tenant:
```bash
bin/pulsar-admin tenants create --admin-roles admin --alowed-clusters standalone investments
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

Note the use of persistent here - it is the default for tenants. If non-persistent, Broker cache is not kept inside the cache = better performance and throughout, however if it fails or Broker crashes you lose all the data