from sqlalchemy.orm import Session
from core.db import models


def get_items(db: Session, item_id_seed: int, n=10):
    return db.query(models.FBT).filter(models.FBT.item_id_seed == item_id_seed).limit(n).all()
