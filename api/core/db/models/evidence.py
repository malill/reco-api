from pydantic import BaseModel, Field, Extra
from bson import ObjectId
from typing import Optional
from datetime import datetime


class BasicEvidenceModel(BaseModel):
    """Basic class that is used for persisting information on user behaviour.

    Attributes: #noqa
        name (str): Description of collection that is tracked (e.g. 'view_details', 'purchase', 'order_entry).
        keys (dict(str, list)): Identifier (1-n assignments) for user, e.g. cookie values, device information, etc.
        item_id (str, optional): Can be used when tracking collection for interaction with items.
        device_info (dict, optional): Capture devices infos to detect mobile/tablet/desktop views.
        path (str, optional): Specific URL path.
        timestamp (datetime): Current timestamp.
    """

    name: str = Field(...)
    keys: dict = Field(...)
    item_id: Optional[str]
    device_info: Optional[dict]
    path: Optional[str]
    cookies: Optional[dict]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        extra = Extra.allow  # additional attributes (not defined above) can also be inserted/retrieved
        schema_extra = {
            "example": {
                "name": "view details",
                "keys": {
                    'cookie': ['cookie_a', 'cookie_b'],
                    'canvas': ['canvas_a', 'canvas_b'],
                    'gp_id': ['123456789']
                },
                "item_id": "item1234",
                "device_info": {
                    "width": 500,
                    "height": 700,
                    "platform": "Win32",
                    "language": "en-EN",
                },
                "path": "https://path-to-step.com"
            }
        }

# TODO: user_id is not well defined (e.g. there needs to be a clearer definition)
# -> maybe user_id comes from recommender system (for internal use only!)
# -> collection 'user' has documents with _id=user_id (reco-system id!)
# -> each user doc, contains a custom dictionary with other collected IDs
# (e.g. "Business Partner ID", "device ID(s)", "reco cookie ID(s)")
# but this means, an collection from an anonymous user (more general a user with a "probabilistic" user_id) needs to
# be updated (user_id needs to be updated) as soon as the true (=deterministic) user_id reveals
# Idea: what about a prob_user_id?
# Idea: this means user_id can not be delivered by frontend or reco-interactor-js, reco-slider-js etc.
# Idea: collection contains user_id but reco systems has user_uid
# should I run an updater on collection collection to add user_uid to collection or should I create a link only
# between user <> collection collection?
# How do I store different user_id(s)? -> key-value pair? What is the key? Better key-array[values] pairs?
# this means frontend identifier need to track an fixed attribute "identifier" which contains a dict, e.g.
# identifier: {device-id: [123456, 654321], gp-id: abcde}
# better: consumer_id (consumer coll. _id) is the reco-based user_id?
# BEST: frontend: user_id, backend: consumer_id, user_id is contained in a list of identifiers of consumer document
# collection can only contain user_id, backend always deals with consumer id?
