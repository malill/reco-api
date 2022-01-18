from datetime import datetime

from pydantic import BaseModel, Field


# TODO: id references (seed, recommended) should contain the mongodb _id and not the id (=attribute of consumable)

class FrequentlyBoughtTogetherRec(BaseModel):
    consumable_id_seed: str = Field()
    consumable_id_recommended: str = Field()
    confidence: float = Field()
    support: float = Field()
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CollaborativeFilteringRec(BaseModel):
    consumable_id_seed: str = Field()
    consumable_id_recommended: str = Field()
    similarity: float = Field()
    base: str = Field(...)  # user/item
    timestamp: datetime = Field(default_factory=datetime.utcnow)
