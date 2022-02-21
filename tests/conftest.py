from motor.motor_asyncio import AsyncIOMotorClient
from pytest import fixture
from starlette.testclient import TestClient

from api.core.db.mongodb import get_database, DataBase
import api.core.util.config as cfg


@fixture(scope="session")
def test_user():
    return {
        "first_name": "Pete",
        "last_name": "Sampras",
        "keys": {"cookie": ["cookie_test"], "ab_test": cfg.ITEM_BASED_COLLABORATIVE_FILTERING},
        "roles": ['b2c_customer', 'u18'],
        "groups": {
            "ab_test": "ibcf"
        }
    }


@fixture(scope="session")
def test_items():
    return [
        {
            "id": "testID1",
            "type": "product",
            "name": "Fancy Test Item"
        },
        {
            "id": "testID2",
            "type": "content",
            "name": "Lame Test Content"
        }
    ]


@fixture(scope="session")
def test_recommendations_ib_cf():
    return [
        {"item_id_seed": "1", "item_id_recommended": "101", "similarity": 0.06, "base": "item"},
        {"item_id_seed": "1", "item_id_recommended": "102", "similarity": 0.07, "base": "item"},
        {"item_id_seed": "1", "item_id_recommended": "103", "similarity": 0.08, "base": "item"},
        {"item_id_seed": "1", "item_id_recommended": "104", "similarity": 0.09, "base": "item"},
        {"item_id_seed": "1", "item_id_recommended": "105", "similarity": 0.1, "base": "item"}
    ]


@fixture(scope="session")
def test_client(test_user):
    from main import app
    with TestClient(app) as test_client:
        yield test_client
