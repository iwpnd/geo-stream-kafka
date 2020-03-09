import pytest
from app.core.models.model import ConsumerResponse
from pydantic import ValidationError


@pytest.mark.parametrize(
    "id, topic, name, timestamp, lat, lon, expectation",
    [
        pytest.param(
            1,
            "topic",
            "name",
            "2020-03-09 09:18:47.761466",
            "52.53",
            "13.37",
            pytest.raises(ValidationError),
            id="latlon as str",
        ),
        pytest.param(
            2,
            "topic",
            5,
            "2020-03-09 09:18:47.761466",
            51.1,
            13.3,
            pytest.raises(ValidationError),
            id="name not str",
        ),
        pytest.param(
            3,
            5,
            "name",
            "2020-03-09 09:18:47.761466",
            51.1,
            13.3,
            pytest.raises(ValidationError),
            id="topic not str",
        ),
        pytest.param(
            4,
            "topic",
            "name",
            "2020-03-09 09:18:47.761466",
            -91,
            13,
            pytest.raises(ValidationError),
            id="lat too small",
        ),
        pytest.param(
            5,
            "topic",
            "name",
            "2020-03-09 09:18:47.761466",
            91,
            13,
            pytest.raises(ValidationError),
            id="lat too big",
        ),
        pytest.param(
            6,
            "topic",
            "name",
            "2020-03-09 09:18:47.761466",
            51.1,
            -181,
            pytest.raises(ValidationError),
            id="lon too small",
        ),
        pytest.param(
            7,
            "topic",
            "name",
            "2020-03-09 09:18:47.761466",
            51.1,
            181,
            pytest.raises(ValidationError),
            id="lon too big",
        ),
    ],
)
def test_consumer_response_raises(id, topic, name, timestamp, lat, lon, expectation):

    with expectation:
        msg = ConsumerResponse(
            topic=topic, name=name, timestamp=timestamp, lat=lat, lon=lon
        )

        assert isinstance(msg, ConsumerResponse)
