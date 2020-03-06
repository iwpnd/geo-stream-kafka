import asyncio
import json

from aiokafka import AIOKafkaProducer
from app.core.models.model import ProducerMessage
from fastapi import FastAPI
from loguru import logger

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


@app.post("/aioproducer/{topicname}")
async def aio_geostream_produce(msg: ProducerMessage, topicname: str):
    logger.debug(topicname)
    logger.debug(aioproducer)
    result = await aioproducer.send_and_wait(
        topicname, json.dumps(msg.dict()).encode("ascii")
    )
    print(result)


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
