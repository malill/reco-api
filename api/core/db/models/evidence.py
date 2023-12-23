from pydantic import BaseModel, Field, Extra
from bson import ObjectId
from typing import Optional
from datetime import datetime


class BasicEvidenceModel(BaseModel):
    """Basic class that is used for persisting information on user behaviour.

    Attributes: #noqa
        name (str): Description of collection that is tracked (e.g. 'view_details', 'purchase', 'order_entry).
        user_uid (str, optional): Unique identifier for user object.
        item_id (str, optional): Can be used when tracking collection for interaction with items.
        path (str, optional): Specific URL path.
        timestamp (datetime): Current timestamp.
    """

    name: str = Field(...)
    user_uid: Optional[str] = Field()
    item_id: Optional[str]
    path: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        exclude_none = True
        extra = Extra.allow  # additional attributes (not defined above) can also be inserted/retrieved
        schema_extra = {
            "example": {
                "name": "view details",
                "user_uid": "123456789",
                "item_id": "item1234",
                "path": "https://path-to-step.com"
            }
        }
