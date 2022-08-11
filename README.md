# Kafka consumer exposing data through Websockets
This project consists of a simple kafka consumer which subscribes to 3 topics and exposes the data that it receives
through websockets using [socket.io](https://python-socketio.readthedocs.io/en/latest/). 
The consumer is supposed to belong to the network of the kafka-cluster that is consuming, and the project is designed
to consume from topics created by the [Distributed Counter with Faust](https://github.com/chrisbek/distributed-counter) 
project, but topic names are configurable.
When the stack is started through docker-compose, a [uvicorn server](https://www.uvicorn.org/) is exposed at 
`http://172.30.1.21:8000` which provides the following socket.io events:

- `register_room`: allows registering a client to one or more rooms, based on an array of identifiers
- `consume_1_min_aggregations`: allows consuming 1 minute aggregation data for all the identifiers for which the client
    has been registered.
- `consume_5_min_aggregations`: allows consuming 5 minute aggregation data for all the identifiers for which the client
    has been registered.
- `consume_10_min_aggregations`: allows consuming 10 minute aggregation data for all the identifiers for which the client
    has been registered.

The aggregated data are sent through websockets to the following socket.io events: `live_aggregations_1`, 
`live_aggregations_5`, `live_aggregations_10`.

> Note that the current project is not optimized for production. In order to have the server in a prod like environment
> one should:
> - Configure `uvicorn` server for production.
> - Place the server behind a load balancer that supports 
> [sticky sessions](https://python-socketio.readthedocs.io/en/latest/server.html#scalability-notes) 
> (e.g. `NginX`, `Traefik` or `AWS ELB`).
> - Configure an adapter for message broadcasting other than in-memory 
> (e.g. [use redis as adapter](https://socket.io/docs/v4/redis-adapter/)).


# Local Setup

## Prerequisites
- docker >= 20.10.17
- docker-compose >= 1.26.2
- make file support
> If your system does not support make files you can manually execute the docker-compose commands in `makefile`.

## Initial configuration
- clone [Distributed Counter with Faust](https://github.com/chrisbek/distributed-counter):
```
git clone git@github.com:chrisbek/distributed-counter.git
```
and start both kafka cluster, and faust consumers _(they are configured to create data for the OBSERVED_VIDEO_IDENTIFIERS
defined in `src/tests/client.py`)_.

- clone this project (`git clone git@github.com:chrisbek/kafka_consumer_websockets.git`)
- start the server:
```
cd /path/to/project
cp ./config/.env.dev ./config/.env -v
make start-consumer
```
> The `main-net` docker network must have been created during the preparation steps of the `Distributed Counter with Faust`.
> This project assumes that the server's container is executed in the same network as the kafka-cluster. If that's not the
> case one should:
>   - properly configure the `KAFKA_ADVERTISED_LISTENERS` of the kafka-cluster.
>   - use the corresponding value advertised by kafka as the `kafka_broker_url` in the server startup
> (configurable through the `KAFKA_BROKER_URL` in the `.env.dev`).

## Inspect containers' logs
You can always inspect the containers' logs using the following commands:
```
docker logs --follow kafka.consumer
```

## Stop stack
- Stop running containers by:
```
make stop-consumer
```

# Test
The SocketIO server is usually consumed by a Frontend application, but we can locally test and debug our solution using
a python client such the one in `src/tests/client.py`.
In order to start the client you need to execute the following steps:
```
cd /path/to/project/
poetry shell
poetry install
cd src/tests
python client.py
```
Requirements:
- install [poetry (dependency manager)](https://python-poetry.org/docs/#installation) to your system
- python3.9-dev should exist on your system (`sudo apt-get install python3.9-dev`)
