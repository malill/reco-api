from typing import List
import logging
from sqlalchemy.orm import Session
from core.db import models
import random
import re

from core.db.models import Item


def limit_returned_items(items, n_recos):
    """ This function should take care of adding items when len(items) < n_recos """
    if len(items) < n_recos:
        logging.warning(f"Number of requested items ({n_recos}) less than number of items ({len(items)}) in database")
    return items[0:n_recos]


def get_random_items(db: Session, n_recos=5) -> List[Item]:
    """Retrieve random items from 'content' db.

    Args:
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of random items.
    """
    rand = random.sample(range(0, db.query(models.Item).count()), n_recos)
    items = db.query(models.Item)
    return list(items[i] for i in rand)


def get_latest_items(db: Session, n_recos=5) -> List[Item]:
    """Retrieve latest added items from 'recs' db.

    Args:
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of most recent items.
    """
    return limit_returned_items(list(db.query(models.Item).order_by(models.Item.creation_time.desc()).limit(n_recos)),
                                n_recos)


def get_frequently_bought_together_items(db: Session, item_id_seed: int, n_recos=5) -> List[Item]:
    """Retrieve frequently bought together items from 'recs' db.

    Args:
        db (Session): Session object used for retrieving items from db.
        item_id_seed (int): ID of seed item that is used for finding frequently bought together items.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of frequently bought together items.
    """
    item_id_seed = quick_fix_adjust_item_id(item_id_seed)
    return limit_returned_items(list(db.query(models.FBT).filter(models.FBT.item_id_seed == item_id_seed).order_by(
        models.FBT.confidence.desc()).limit(n_recos)), n_recos)


def get_item_based_collaborative_filtering_items(db: Session, item_id_seed: int, n_recos=5) -> List[Item]:
    """Retrieve item based collaborative filtered items from 'recs' db.

    Args:
        db (Session): Session object used for retrieving items from db.
        item_id_seed (int): ID of seed item that is used for finding similar items.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of similar (item-wise) items.
    """
    item_id_seed = quick_fix_adjust_item_id(item_id_seed)
    return limit_returned_items(list(db.query(models.ICF).filter(models.ICF.item_id_seed == item_id_seed).order_by(
        models.ICF.similarity.desc()).limit(n_recos)), n_recos)


def quick_fix_adjust_item_id(item_id: int):
    """ quick fix for variants """
    if len(str(item_id)) > 4:
        item_id = str(item_id)[:-3]
    return int(item_id)
