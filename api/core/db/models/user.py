from typing import Optional
from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field, Extra


class Reco2jsModel(BaseModel):
    """This is the hash that will be send to API for unique user identification. Created a class since hash might
    require postprocessing (to encrypt canvas-, cookie-, audio- etc. keys).

    Attributes: #noqa
        id (str): Identifier created by reco2.js."""
    id: Optional[str] = Field(...)


class BasicUserKeys(BaseModel):
    """Identifier(1 - n assignments) for user, e.g.cookie values, device information, etc. Class is only used to
    handle user keys, not persisted in MongoDB."""
    reco2js_ids: list | None = None  # list of reco2.js IDs
    cookies: list | None = None
    canvas: list | None = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        extra = Extra.allow
        # json_schema_extra = {
        #     "example": {
        #         'cookie': ['cookie_a', 'cookie_b'],
        #         'canvas': ['canvas_a', 'canvas_b'],
        #     }
        # }


class BasicUserModel(BaseModel):
    """Basic class used to persist user information.

    Attributes: #noqa
        keys (BasicUserKeys): Identifier (1-n assignments) for user, e.g. cookie values, device information, etc.
        first_name (str, optional): User first name
        last_name (str, optional): User last name
        roles (list, optional): User roles, e.g. membership(s), preference(s) etc.
        groups (dict(str, str), optional): 1-1 assignments of user to groups with values
        devices: (dict(str, dict), optional): Dictionary of user devices {reco2jsID1: {**device1Info}}, reco2jsID2: ...
    """
    keys: BasicUserKeys = Field()
    first_name: Optional[str]
    last_name: Optional[str]
    roles: Optional[list]
    groups: Optional[dict]
    devices: Optional[dict]
    update_time: datetime = Field(default_factory=datetime.utcnow)

    def get_uid(self):
        return self.__getattribute__('_id')

    def __str__(self):
        return str(self.__getattribute__('_id'))

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        extra = Extra.allow
        # json_schema_extra = {
        #     "example": {
        #         "first_name": "Jane",
        #         "last_name": "Doe",
        #         "keys": {
        #             'cookie': ['cookie_a', 'cookie_b'],
        #             'canvas': ['canvas_a', 'canvas_b'],
        #             'gp_id': ['123456789']
        #         },
        #         "roles": {"fantasy_league", "b2b_customer"},
        #         "groups": {
        #             "splitting1": "cf_ib"
        #         }
        #     }
        # }


dummy_user_dict = {"_id": "Dummy", "first_name": "Dummy", "last_name": "Dummy", "keys": BasicUserKeys()}
