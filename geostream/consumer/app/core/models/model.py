from datetime import datetime

from pydantic import BaseModel
from pydantic import StrictStr
from pydantic import validator


class ConsumerResponse(BaseModel):
    topic: StrictStr
    timestamp: str
    data: dict

    @validator("timestamp", pre=True, always=True)
    def unix_to_str(cls, v):
        return str(datetime.utcfromtimestamp(int(v) / 1000))
