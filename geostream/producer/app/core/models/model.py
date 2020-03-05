import uuid
from datetime import datetime

from pydantic import BaseModel
from pydantic import confloat
from pydantic import StrictStr
from pydantic import validator


class ProducerMessage(BaseModel):
    name: StrictStr
    message_id: StrictStr = ""
    timestamp: StrictStr = str(datetime.utcnow())
    lat: confloat(gt=-90, lt=90)
    lon: confloat(gt=-180, lt=180)

    @validator("message_id", pre=True, always=True)
    def set_id_from_name_uuid(cls, v, values):
        if "name" in values:
            return f"{values['name']}_{uuid.uuid4()}"
        else:
            raise ValueError("name not set")
