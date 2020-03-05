from app.core.models.model import ProducerMessage
from fastapi import FastAPI
from pykafka import KafkaClient

app = FastAPI()

client = KafkaClient(hosts="kafka:9092")


@app.post("/producer/{topicname}")
async def geostream_produce(msg: ProducerMessage, topicname: str):
    # topic = client.topics[topicname]
    # producer = topic.get_sync_producer()
    # producer.produce("{}".format(msg.dict()).encode("ascii"))
    return msg


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
