from datetime import datetime

from pydantic import BaseModel, Field


# TODO: id references (seed, recommended) should contain the mongodb _id and not the id (=attribute of item)

class FrequentlyBoughtTogetherRec(BaseModel):
    item_id_seed: str = Field()
    item_id_recommended: str = Field()
    confidence: float = Field()
    support: float = Field()
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CollaborativeFilteringRec(BaseModel):
    item_id_seed: str = Field()
    item_id_recommended: str = Field()
    similarity: float = Field()
    base: str = Field(...)  # user/item
    timestamp: datetime = Field(default_factory=datetime.utcnow)
