import asyncio
import json

from aiokafka import AIOKafkaProducer
from app.core.models.model import ProducerMessage
from fastapi import FastAPI
from loguru import logger

app = FastAPI()

loop = asyncio.get_event_loop()
aioproducer = AIOKafkaProducer(
    loop=loop, client_id="geostream-kafka", bootstrap_servers="kafka:9092"
)


@app.on_event("startup")
async def startup_event():
    await aioproducer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await aioproducer.stop()


@app.post("/producer/{topicname}")
async def kafka_produce(msg: ProducerMessage, topicname: str):

    result = await aioproducer.send_and_wait(
        topicname, json.dumps(msg.dict()).encode("ascii")
    )

    logger.debug(result)


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
