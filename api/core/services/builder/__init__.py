from typing import Generic, TypeVar
import api.core.util.config as cfg
from api.core.db.mongodb_utils import MongoDBHelper
from api.core.util.config import DB_NAME

T = TypeVar('T')


class BaseRecoBuilder(Generic[T]):
    """
    All builders inherit BaseRecoBuilder and need to provide following methods and attributes.

    attributes:
    - relations: list[Generic[T]]
            each list entry contains an instance of reco model
    - collection_name: str
            the collection of database where relations can be persisted

    methods:
    - run(self): None
            performing run() on an instance of a builder class calculates
            the relations and stores them in attribute relations (see above)
    - store_relations(self): None
            persists relations in self.collection_name of database (from .env)
    """

    def __init__(self):
        self.relations: [T] = []

    def run(self):
        return

    def store_relations(self):
        with MongoDBHelper(DB_NAME) as db:
            db[cfg.COLLECTION_NAME_RELATIONS].insert_many([rec.dict(by_alias=True) for rec in self.relations])
