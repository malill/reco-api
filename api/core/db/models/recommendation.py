from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


# TODO: id references (seed, recommended) should contain the mongodb _id and not the id (=attribute of item)

class ABTestModel(BaseModel):
    """Model for A/B Testing Configuration.

    Attributes: #noqa
        name (str): A/B testing name.
        methods (List[str]): List of strings that are considered as recommendation method shortcuts.
        timestamp (datetime): Current timestamp.
    """
    name: str = Field()
    methods: List[str] = Field()
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class BasicRecommendationModel(BaseModel):
    """BaseModel of a recommendation entry.

    Attributes: #noqa
        type (str): Recommendation algorithm used for entry, e.g. ib_cf, fbt, etc.
        item_id_seed (str): ID of item for which recommendations are needed.
        item_id_recommended (str): ID of recommended item.
        timestamp (datetime): Current timestamp.
    """
    type: str = Field()
    item_id_seed: str = Field()
    item_id_recommended: str = Field()
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CollaborativeFilteringRec(BasicRecommendationModel):
    """Recommendation entry for collaborative filtering algorithm.

    Attributes: #noqa
        similarity (float): Metric of collaborative filtering.
        base (str): Type of filtering, i.e. "item" or "used"
    """
    similarity: float = Field()
    base: str = Field(...)  # user/item


class FrequentlyBoughtTogetherRec(BasicRecommendationModel):
    """Recommendation entry based on frequently bought together association rule.

    Attributes: #noqa
        confidence (float): Metric of frequently bought together.
        support (float): Metric of frequently bought together.
    """
    confidence: float = Field()
    support: float = Field()
