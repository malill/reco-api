from typing import List
import logging
from sqlalchemy.orm import Session
from core.db import models
import random

from core.db.models import Item


def sort_by_metric(items, sorting_type, n_recos):
    try:
        items.sort(key=lambda i: getattr(i, sorting_type), reverse=True)
    except AttributeError:
        logging.error(f"Could not perform sorting '{sorting_type}' ... use unfiltered response from DB")
    return limit_returned_items(items, n_recos)


def limit_returned_items(items, n_recos):
    if len(items) < n_recos:
        logging.warning("Number of requested items less than number of items in database")
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


def get_frequently_bought_together_items(db: Session, item_id_seed: int, n_recos=5) -> List[Item]:
    """Retrieve frequently bought together items from 'recs' db.

    Args:
        db (Session): Session object used for retrieving items from db.
        item_id_seed (int): ID of seed item that is used for finding frequently bought together items.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of frequently bought together items.
    """
    return sort_by_metric(
        db.query(models.FBT).filter(models.FBT.item_id_seed == item_id_seed).all(),
        "confidence",
        n_recos)


def get_item_based_collaborative_filtering_items(db: Session, item_id_seed: int, n_recos=5) -> List[Item]:
    """Retrieve item based collaborative filtered items from 'recs' db.

    Args:
        db (Session): Session object used for retrieving items from db.
        item_id_seed (int): ID of seed item that is used for finding similar items.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of similar (item-wise) items.
    """
    return sort_by_metric(
        db.query(models.ICF).filter(models.ICF.item_id_seed == item_id_seed).all(),
        "similarity",
        n_recos)
