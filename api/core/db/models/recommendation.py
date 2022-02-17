from datetime import datetime

from pydantic import BaseModel, Field


# TODO: id references (seed, recommended) should contain the mongodb _id and not the id (=attribute of item)

class ABTest(BaseModel):
    name: str = Field()


class CollaborativeFilteringRec(BaseModel):
    """Recommendation entry for collaborative filtering algorithm.

    Attributes:
        item_id_seed (str): ID of item for which recommendations are needed.
        item_id_recommended (str): ID of recommended item.
        similarity (float): Metric of collaborative filtering.
        base (str): Type of filtering, i.e. "item" or "used"
        timestamp (datetime): Current timestamp.
    """
    item_id_seed: str = Field()
    item_id_recommended: str = Field()
    similarity: float = Field()
    base: str = Field(...)  # user/item
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class FrequentlyBoughtTogetherRec(BaseModel):
    """Recommendation entry based on frequently bought together association rule.

    Attributes:
        item_id_seed (str): ID of item for which recommendations are needed.
        item_id_recommended (str): ID of recommended item.
        confidence (float): Metric of frequently bought together.
        support (float): Metric of frequently bought together.
        timestamp (datetime): Current timestamp.
    """
    item_id_seed: str = Field()
    item_id_recommended: str = Field()
    confidence: float = Field()
    support: float = Field()
    timestamp: datetime = Field(default_factory=datetime.utcnow)
