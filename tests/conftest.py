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
        "keys": {"cookie": ["cookie_test"]},
        "roles": ['u18', 'b2c_customer']
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
def test_client(test_user):
    from main import app
    with TestClient(app) as test_client:
        yield test_client
