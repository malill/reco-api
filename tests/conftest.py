import json

from pytest import fixture
from starlette.testclient import TestClient

import api.core.util.config as cfg
from api.core.db.models.relation import CollaborativeFilteringRelation


@fixture(scope="session")
def test_client():
    from main import app
    with TestClient(app) as test_client:
        yield test_client


@fixture(scope="session")
def test_user1():
    return {
        "first_name": "Pete",
        "last_name": "Sampras",
        "keys": {"cookie": ["petes_cookie"], "canvas": ["01234", "56789"]},
        "roles": ['shooter', 'english'],
        "groups": {
            "split1": cfg.TYPE_ITEM_BASED_COLLABORATIVE_FILTERING
        }
    }


@fixture(scope="session")
def test_user2():
    return {
        "first_name": "Raphael",
        "last_name": "Nadal",
        "keys": {"cookie": ["raphaels_cookie"], "canvas": ["abcde", "fghij"]},
        "roles": ['left_handed'],
        "groups": {
            "ab_test2": cfg.TYPE_ITEM_BASED_COLLABORATIVE_FILTERING
        }
    }


@fixture(scope="session")
def test_items():
    with open('tests/mock/items.json') as json_file:
        data = json.load(json_file)
    return data


@fixture(scope="session")
def test_relations_ib_cf():
    relations = [
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
    res = [CollaborativeFilteringRelation(**rec) for rec in relations]
    return res


@fixture(scope="session")
def test_evidence():
    with open('tests/mock/evidence.json') as json_file:
        data = json.load(json_file)
    return data


@fixture(scope="session")
def test_splitting1():
    return [cfg.TYPE_RANDOM_RECOMMENDATIONS, cfg.TYPE_ITEM_BASED_COLLABORATIVE_FILTERING]


@fixture(scope="session")
def test_splitting2():
    return [cfg.TYPE_RANDOM_RECOMMENDATIONS, cfg.TYPE_ITEM_BASED_COLLABORATIVE_FILTERING]
