from pydantic import BaseModel
from pydantic import confloat
from pydantic import StrictStr


class ConsumerResponse(BaseModel):
    topic: StrictStr
    timestamp: str
    name: StrictStr
    message_id: StrictStr
    lat: confloat(gt=-90, lt=90)
    lon: confloat(gt=-180, lt=180)
