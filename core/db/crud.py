from sqlalchemy.orm import Session
from core.db import models
import random


def get_random_items(db: Session, n_recos=5):
    rand = random.sample(range(0, db.query(models.Item).count()), n_recos)
    items = db.query(models.Item)
    return list(items[i] for i in rand)


def get_frequently_bought_together_items(db: Session, item_id_seed: int, n_recos=5):
    return db.query(models.FBT).filter(models.FBT.item_id_seed == item_id_seed).limit(n_recos).all()
