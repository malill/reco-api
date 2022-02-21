from typing import Generic, TypeVar

from api.core.db.mongodb_utils import MongoDBHelper
from api.core.util.config import DB_NAME

T = TypeVar('T')


class BaseRecoBuilder(Generic[T]):
    """
    All builders inherit BaseRecoBuilder and provide following methods and attributes.

    attributes:
    - recs: list[Generic[T]]
            each list entry contains an instance of recommendation model
    - collection_name: str
            the collection of database where recommendations can be persisted

    methods:
    - run(self): None
            performing run() on an instance of a builder class calculates
            the recommendations and stores them in attribute recs (see above)
    - store_recs(self): None
            persists recommendations in self.collection_name of database (from .env)
    """

    def __init__(self, collection_name):
        self.recs: [T] = []
        # legacy attribute, recs are stored in single collection - differentiation between recs field "type"
        self.collection_name = collection_name

    def run(self):
        return

    def store_recs(self):
        with MongoDBHelper(DB_NAME) as db:
            db[self.collection_name].insert_many([rec.dict(by_alias=True) for rec in self.recs])
