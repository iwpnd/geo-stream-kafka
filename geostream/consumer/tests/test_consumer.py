import asyncio

import pytest


def test_get_consumer(test_app, monkeypatch):
    pass


@pytest.mark.asyncio
async def test_consumer_websocket(test_app):
    with test_app.websocket_connect("/consumer/geostream") as websocket:
        data = websocket.receive_json()
        await asyncio.sleep(0.1)

    assert data == {"Message: ": "connected"}
