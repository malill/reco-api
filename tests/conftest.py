from motor.motor_asyncio import AsyncIOMotorClient
from pytest import fixture
from starlette.testclient import TestClient

import api.core.util.config as cfg
from api.core.db.models.recommendation import CollaborativeFilteringRec
from api.core.db.mongodb import DataBase


@fixture(scope="session")
def test_client():
    from main import app
    with TestClient(app) as test_client:
        yield test_client


@fixture(scope="session")
def test_user():
    return {
        "first_name": "Pete",
        "last_name": "Sampras",
        "keys": {"cookie": ["petes_cookie"], "canvas": ["01234", "56789"]},
        "roles": ['b2c_customer', 'u18'],
        "groups": {
            "ab_test1": cfg.TYPE_ITEM_BASED_COLLABORATIVE_FILTERING
        }
    }


@fixture(scope="session")
def test_product_items():
    return [
        {"id": "1", "type": "product", "name": "Fancy Test Item 1"},
        {"id": "2", "type": "product", "name": "Fancy Test Item 2"},
        {"id": "3", "type": "product", "name": "Fancy Test Item 3"},
        {"id": "4", "type": "product", "name": "Fancy Test Item 4"},
        {"id": "5", "type": "product", "name": "Fancy Test Item 5"},
        {"id": "6", "type": "product", "name": "Fancy Test Item 6"},
    ]


@fixture(scope="session")
def test_recommendations_ib_cf():
    recs = [
        {"type": cfg.TYPE_ITEM_BASED_COLLABORATIVE_FILTERING, "item_id_seed": "1", "item_id_recommended": "101",
         "similarity": 0.06, "base": "item"},
        {"type": cfg.TYPE_ITEM_BASED_COLLABORATIVE_FILTERING, "item_id_seed": "1", "item_id_recommended": "102",
         "similarity": 0.07, "base": "item"},
        {"type": cfg.TYPE_ITEM_BASED_COLLABORATIVE_FILTERING, "item_id_seed": "1", "item_id_recommended": "103",
         "similarity": 0.08, "base": "item"},
        {"type": cfg.TYPE_ITEM_BASED_COLLABORATIVE_FILTERING, "item_id_seed": "1", "item_id_recommended": "104",
         "similarity": 0.09, "base": "item"},
        {"type": cfg.TYPE_ITEM_BASED_COLLABORATIVE_FILTERING, "item_id_seed": "1", "item_id_recommended": "105",
         "similarity": 0.1, "base": "item"}
    ]
    res = [CollaborativeFilteringRec(**rec) for rec in recs]
    return res
