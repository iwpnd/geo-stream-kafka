import asyncio
import json

from aiokafka import AIOKafkaConsumer
from app.core.config import KAFKA_INSTANCE
from app.core.config import PROJECT_NAME
from app.core.models.model import ConsumerResponse
from fastapi import FastAPI
from fastapi import WebSocket
from loguru import logger
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(title=PROJECT_NAME)
app.add_middleware(CORSMiddleware, allow_origins=["*"])


async def consume(topicname):
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer(
        topicname,
        loop=loop,
        client_id=PROJECT_NAME,
        bootstrap_servers=KAFKA_INSTANCE,
        # group_id="my_group",
        enable_auto_commit=False,
        session_timeout_ms=10000,
        connections_max_idle_ms=120000,
    )

    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            return msg.value.decode()

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


@app.websocket("/consumer/{topicname}")
async def kafka_consumer_ws(websocket: WebSocket, topicname: str):
    """
    Consume messages from <topicname>

    This will start a Kafka Consumer from a topic

    And this path operation will:

    * return ConsumerResponse
    """

    await websocket.accept()
    while True:
        data = await consume(topicname)
        response = ConsumerResponse(topic=topicname, **json.loads(data))
        logger.debug(response)
        await websocket.send_text(f"{response.json()}")


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
