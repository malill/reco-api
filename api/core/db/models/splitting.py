from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class SplittingModel(BaseModel):
    """Model for A/B (Bayesian, etc.) testing configuration.

    Attributes: #noqa
        name (str): Splitting testing name.
        methods (List[str]): List of strings that are considered as reco method shortcuts.
        timestamp (datetime): Current timestamp.
    """
    name: str = Field()
    methods: List[str] = Field()
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    # TODO: define allowed string values for methods
