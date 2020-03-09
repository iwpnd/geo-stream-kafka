import asyncio

from aiokafka import AIOKafkaConsumer
from app.core.config import KAFKA_INSTANCE
from app.core.config import PROJECT_NAME
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

# from app.core.models.model import ConsumerResponse
# from loguru import logger

app = FastAPI(title=PROJECT_NAME)
app.add_middleware(CORSMiddleware, allow_origins=["*"])


async def consume(topicname):
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer(
        topicname,
        loop=loop,
        client_id=PROJECT_NAME,
        bootstrap_servers=KAFKA_INSTANCE,
        group_id="my_group",
        enable_auto_commit=False,
        session_timeout_ms=10000,
        connections_max_idle_ms=120000,
    )

    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            return msg.value

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://127.0.0.1:8003/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await consume("geostream")
        await websocket.send_text(f"Message text was: {data}")


# @app.get("/consumer/{topicname}")
# async def kafka_consume(topicname: str):
#     """
#     Consume messages from <topicname>

#     This will start a Kafka Consumer from a topic

#     And this path operation will:

#     * return ConsumerResponse
#     """
#     cr = ConsumerResponse()
#     print(cr)
#     msg = await consume(topicname)
#     logger.info(msg.decode())

#     return msg


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
