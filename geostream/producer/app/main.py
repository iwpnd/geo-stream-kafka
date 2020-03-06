import asyncio
import json

from aiokafka import AIOKafkaProducer
from app.core.models.model import ProducerMessage
from fastapi import FastAPI
from loguru import logger
from pykafka import KafkaClient

app = FastAPI()

aioproducer = None


@app.on_event("startup")
async def startup_event():
    global aioproducer
    loop = asyncio.get_event_loop()
    aioproducer = AIOKafkaProducer(loop=loop, bootstrap_servers="kafka:9092")

    await aioproducer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await aioproducer.stop()


client = KafkaClient(hosts="kafka:9092")
topic = client.topics["geostream"]
producer = topic.get_sync_producer()


@app.post("/producer/{topicname}")
async def geostream_produce(msg: ProducerMessage, topicname: str):
    logger.debug(topicname)
    logger.debug(producer)
    producer.produce(json.dumps(msg.dict()).encode("ascii"))


@app.post("/aioproducer/{topicname}")
async def aio_geostream_produce(msg: ProducerMessage, topicname: str):
    logger.debug(topicname)
    logger.debug(producer)
    result = await aioproducer.send_and_wait(
        topicname, json.dumps(msg.dict()).encode("ascii")
    )
    print(result)


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
