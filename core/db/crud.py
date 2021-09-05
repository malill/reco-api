from sqlalchemy.orm import Session
from core.db import models


def get_items(db: Session, item_seed_id: int, n=3):
    return db.query(models.FBT).filter(models.FBT.item_seed_id == item_seed_id).limit(n).all()
