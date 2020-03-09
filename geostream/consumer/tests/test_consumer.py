def test_get_consumer(test_app, monkeypatch):
    pass


def test_consumer_websocket(test_app):
    with test_app.websocket_connect("/consumer/geostream") as websocket:
        data = websocket.receive_json()
    websocket.close()

    assert data == {"connected_to": "geostream"}
