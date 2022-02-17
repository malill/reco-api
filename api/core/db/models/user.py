from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, Extra


class BasicUserModel(BaseModel):
    keys: dict = Field()
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        extra = Extra.allow
        schema_extra = {
            "example": {
                "first_name": "Jane",
                "last_name": "Doe",
                "keys": {
                    'cookie': ['cookie_a', 'cookie_b'],
                    'canvas': ['canvas_a', 'canvas_b'],
                    'gp_id': ['123456789']
                }
            }
        }
