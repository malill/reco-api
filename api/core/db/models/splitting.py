from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class SplittingModel(BaseModel):
    """Model for A/B Testing Configuration.

    Attributes: #noqa
        name (str): A/B testing name.
        methods (List[str]): List of strings that are considered as recommendation method shortcuts.
        timestamp (datetime): Current timestamp.
    """
    name: str = Field()
    methods: List[str] = Field()
    timestamp: datetime = Field(default_factory=datetime.utcnow)
