from datetime import datetime

from pydantic import BaseModel, Field


class FrequentlyBoughtTogetherRec(BaseModel):
    consumable_id_seed: int = Field()
    consumable_id_recommended: int = Field()
    confidence: float = Field()
    support: float = Field()
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CollaborativeFilteringRec(BaseModel):
    consumable_id_seed: int = Field()
    consumable_id_recommended: int = Field()
    similarity: float = Field()
    base: str = Field(...)  # user/item
    timestamp: datetime = Field(default_factory=datetime.utcnow)
