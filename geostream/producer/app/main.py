import asyncio
import json

from aiokafka import AIOKafkaProducer
from app.core.config import KAFKA_INSTANCE
from app.core.config import PROJECT_NAME
from app.core.models.model import ProducerMessage
from app.core.models.model import ProducerResponse
from fastapi import FastAPI
from loguru import logger

app = FastAPI(title=PROJECT_NAME)


loop = asyncio.get_event_loop()
aioproducer = AIOKafkaProducer(
    loop=loop, client_id=PROJECT_NAME, bootstrap_servers=KAFKA_INSTANCE
)


@app.on_event("startup")
async def startup_event():
    await aioproducer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await aioproducer.stop()


@app.post("/producer/{topicname}")
async def kafka_produce(msg: ProducerMessage, topicname: str):
    """
    Produce a message into <topicname>

    This will produce a message into a Apache Kafka topic

    And this path operation will:

    * return ProducerResponse
    """

    result = await aioproducer.send_and_wait(
        topicname, json.dumps(msg.dict()).encode("ascii")
    )

    logger.info(result)

    response = ProducerResponse(
        name=msg.name,
        message_id=msg.message_id,
        topic=topicname,
        timestamp=result.timestamp,
    )

    return response


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
