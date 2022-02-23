from pytest import fixture
from starlette.testclient import TestClient

import api.core.util.config as cfg
from api.core.db.models.recommendation import CollaborativeFilteringRec


@fixture(scope="session")
def test_user():
    return {
        "first_name": "Pete",
        "last_name": "Sampras",
        "keys": {"cookie": ["petes_cookie"], "canvas": ["01234", "56789"]},
        "roles": ['b2c_customer', 'u18'],
        "groups": {
            "ab_test1": cfg.ITEM_BASED_COLLABORATIVE_FILTERING
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
    recs = [
        {"type": cfg.ITEM_BASED_COLLABORATIVE_FILTERING, "item_id_seed": "1", "item_id_recommended": "101",
         "similarity": 0.06, "base": "item"},
        {"type": cfg.ITEM_BASED_COLLABORATIVE_FILTERING, "item_id_seed": "1", "item_id_recommended": "102",
         "similarity": 0.07, "base": "item"},
        {"type": cfg.ITEM_BASED_COLLABORATIVE_FILTERING, "item_id_seed": "1", "item_id_recommended": "103",
         "similarity": 0.08, "base": "item"},
        {"type": cfg.ITEM_BASED_COLLABORATIVE_FILTERING, "item_id_seed": "1", "item_id_recommended": "104",
         "similarity": 0.09, "base": "item"},
        {"type": cfg.ITEM_BASED_COLLABORATIVE_FILTERING, "item_id_seed": "1", "item_id_recommended": "105",
         "similarity": 0.1, "base": "item"}
    ]
    res = [CollaborativeFilteringRec(**rec) for rec in recs]
    return res


@fixture(scope="session")
def test_client(test_user):
    from main import app
    with TestClient(app) as test_client:
        yield test_client
