from typing import Optional
from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field, Extra

from api.core.db.models.PydanticObjectId import PydanticObjectId


class BasicUserKeys(BaseModel):
    """Identifier(1 - n assignments) for user, e.g.cookie values, device information, etc. Class is only used to
    handle user keys, not persisted in MongoDB."""
    cookie: Optional[list]
    canvas: Optional[list]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        extra = Extra.allow
        schema_extra = {
            "example": {
                'cookie': ['cookie_a', 'cookie_b'],
                'canvas': ['canvas_a', 'canvas_b'],
            }
        }


class BasicUserModel(BaseModel):
    """Basic class used to persist user information.

    Attributes: #noqa
        keys (BasicUserKeys): Identifier (1-n assignments) for user, e.g. cookie values, device information, etc.
        first_name (str, optional): User first name
        last_name (str, optional): User last name
        roles (list, optional): User roles, e.g. membership(s), preference(s) etc.
        groups (dict(str, str), optional): 1-1 assignments of user to groups with values
    """
    keys: BasicUserKeys = Field()
    first_name: Optional[str]
    last_name: Optional[str]
    roles: Optional[list]
    groups: Optional[dict]
    update_time: datetime = Field(default_factory=datetime.utcnow)

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
                },
                "roles": {"fantasy_league", "b2b_customer"},
                "groups": {
                    "splitting1": "cf_ib"
                }
            }
        }
