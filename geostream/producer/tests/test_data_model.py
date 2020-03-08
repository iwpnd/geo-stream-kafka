import pytest
from app.core.models.model import ProducerMessage
from app.core.models.model import ProducerResponse
from pydantic import ValidationError


def test_producer_message():
    msg = ProducerMessage(name="messager_1", lat=51.1, lon=13.3)

    assert all(
        [k in msg.dict() for k in ["name", "message_id", "lat", "lon", "timestamp"]]
    )
    assert isinstance(msg.timestamp, str)
    assert isinstance(msg.lat, float)
    assert isinstance(msg.lon, float)


@pytest.mark.parametrize(
    "id, name, lat, lon, expectation",
    [
        pytest.param(
            1,
            "messenger_1",
            "test",
            "test",
            pytest.raises(ValidationError),
            id="latlon as str",
        ),
        pytest.param(
            2, 1, 51.1, 13.3, pytest.raises(ValidationError), id="name as float"
        ),
        pytest.param(
            3,
            "messenger_3",
            -91,
            13,
            pytest.raises(ValidationError),
            id="lat too small",
        ),
        pytest.param(
            4, "messenger_4", 91, 13, pytest.raises(ValidationError), id="lat too big"
        ),
        pytest.param(
            5,
            "messenger_5",
            51.1,
            -181,
            pytest.raises(ValidationError),
            id="lon too small",
        ),
        pytest.param(
            6,
            "messenger_6",
            51.1,
            181,
            pytest.raises(ValidationError),
            id="lon too big",
        ),
    ],
)
def test_producer_message_raises(id, name, lat, lon, expectation):

    with expectation:
        msg = ProducerMessage(name=name, lat=lat, lon=lon)

        assert isinstance(msg, ProducerMessage)


@pytest.mark.parametrize(
    "id, name, message_id, topic, timestamp, expectation",
    [
        pytest.param(
            1,
            "messenger_1",
            "messenger_1_01f6c2d1-6bdd-4ba0-98ab-2f00a816bc57",
            "test",
            1583656501779,
            "2020-03-08 08:35:01.779000",
            id="timestamp to string",
        )
    ],
)
def test_producer_response_timestamp_conversion(
    id, name, message_id, topic, timestamp, expectation
):

    response = ProducerResponse(
        name=name, message_id=message_id, topic=topic, timestamp=timestamp
    )

    assert response.timestamp == expectation
