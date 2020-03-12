# geo-stream-kafka

<p align="center">
<img src="/img/geostream-fastapi-kafka.png" alt="setup geostream fastapi aiokafka">
</p>

<p align="center">
<img src="/img/geostream.gif" alt="geostream gif">
</p>

see [blogpost](https://iwpnd.pw/articles/2020-03/apache-kafka-fastapi-geostream) for a more detailed description

```bash
docker-compose up -d
```

If you're on MacOS set an environment variable like:
```bash
export DOCKER_KAFKA_HOST=$(ipconfig getifaddr en0)
```

that is afterwards used in `docker-compose.yml` to identify the `KAFKA_ADVERTISED_HOST_NAME`. Some similar workaround has to exist for Windows users.
For linux I assume you can just set it to `localhost` if you're only running on Kafka node. See [github.com/wurstmeister/kafka-docker/wiki/Connectivity](https://github.com/wurstmeister/kafka-docker/wiki/Connectivity).

## Kafka
Kafka will be served on `localhost:9092`

## Frontend
open `/geostream/frontend/app/index.html` and associated `map.js` will consume messages when they come in

## Producer
can produce messages to a topic at `localhost:8002/producer/<topicname>`

## Consumer
can consume kafka messages through at `localhost:8003/consumer/<topicname>`
