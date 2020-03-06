from app.core.models.model import ProducerMessage
from fastapi import FastAPI
from pykafka import KafkaClient

app = FastAPI()

client = KafkaClient(hosts="kafka:9092")
topic = client.topics["geostream"]
producer = topic.get_sync_producer()


@app.post("/producer/{topicname}")
async def geostream_produce(msg: ProducerMessage, topicname: str):

    producer.produce("{}".format(msg.dict()).encode("ascii"))


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
