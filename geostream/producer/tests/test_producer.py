from collections import namedtuple

from aiokafka import AIOKafkaProducer


def test_post_producer(test_app):

    msg = {"name": "AIOmessenger_ONE", "lat": 13, "lon": 37}

    topicname = "geostream"

    with test_app as client:
        response = client.post(f"/producer/{topicname}", json=msg)

    assert response.status_code == 200


def test_post_producer_monkey(test_app, monkeypatch):

    msg = {"name": "AIOmessenger_ONE", "lat": 13, "lon": 37}
    topicname = "geostream"

    response = {
        "name": "AIOmessenger_ONE",
        "message_id": "AIOmessenger_ONE_2ab9c8b5-714e-41f2-b1c1-b530a492a05d",
        "topic": "geostream",
        "timestamp": 1583656501779,
    }

    test = namedtuple("response", ["name", "message_id", "topic", "timestamp"])

    response_nt = test(**response)

    async def mock_send(one, two, three):
        return response_nt

    monkeypatch.setattr(AIOKafkaProducer, "send_and_wait", mock_send)

    response = test_app.post(f"/producer/{topicname}", json=msg)

    assert response.status_code == 200
    assert response.json()["name"] == "AIOmessenger_ONE"
