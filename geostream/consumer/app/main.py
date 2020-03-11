import asyncio
import json
import typing

from aiokafka import AIOKafkaConsumer
from app.core.config import KAFKA_INSTANCE
from app.core.config import PROJECT_NAME
from app.core.models.model import ConsumerResponse
from fastapi import FastAPI
from fastapi import WebSocket
from loguru import logger
from starlette.endpoints import WebSocketEndpoint
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


@app.websocket_route("/consumer/{topicname}")
class WebsocketConsumer(WebSocketEndpoint):
    """
    Consume messages from <topicname>

    This will start a Kafka Consumer from a topic

    And this path operation will:

    * return ConsumerResponse
    """

    async def on_connect(self, websocket: WebSocket) -> None:
        topicname = websocket["path"].split("/")[2]  # until I figure out an alternative

        await websocket.accept()
        await websocket.send_json({"Message: ": "connected"})

        self.consumer_task = asyncio.create_task(
            self.send_consumer_message(websocket=websocket, topicname=topicname)
        )

        logger.info("connected")

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        self.consumer_task.cancel()
        logger.info(f"counter: {self.counter}")
        logger.info("disconnected")

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        await websocket.send_json({"Message: ": data})

    async def send_consumer_message(self, websocket: WebSocket, topicname: str) -> None:
        self.counter = 0
        while True:
            data = await consume(topicname)
            response = ConsumerResponse(topic=topicname, **json.loads(data))
            logger.info(response)
            await websocket.send_text(f"{response.json()}")
            self.counter = self.counter + 1


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
