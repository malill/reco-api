import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.testclient import TestClient
import api.core.services.item as service_item
from api.core.db.models.item import BasicItemModel
from api.core.db.mongodb import DataBase
from main import app
import api.core.util.config as cfg


@pytest.fixture(scope='session')
def db():
    db = DataBase()
    db.client = AsyncIOMotorClient(cfg.DB_URL,
                                   maxPoolSize=10,
                                   minPoolSize=10)
    return db


@pytest.fixture(scope='session')
def client():
    client = TestClient(app)
    return client


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200


def test_redirect(client):
    response = client.get("/")
    assert response.request.path_url == "/docs"


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
async def test_insert_item(db):
    items = [
        BasicItemModel(id="testID1", type="product", name="TestItem"),
        BasicItemModel(id="testID2", type="content", name="TestContent")
    ]
    res = await service_item.create_or_update_items(db.client, items)
    assert res.status_code == 201
