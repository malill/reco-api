from motor.motor_asyncio import AsyncIOMotorClient

import api.core.util.config as cfg
from api.core.db.mongodb import DataBase


async def test_prepare_db():
    # TODO: find local option for test MongoDB
    db = DataBase()
    db.client = AsyncIOMotorClient(cfg.DB_URL,
                                   maxPoolSize=10,
                                   minPoolSize=10)
    if "testing" in cfg.DB_NAME.lower():
        # this is dangerous since if test environmental variable DB_NAME is not set properly it could
        # delete productive data
        await db.client[cfg.DB_NAME][cfg.COLLECTION_NAME_ITEM].drop()
        await db.client[cfg.DB_NAME][cfg.COLLECTION_NAME_USER].drop()


def test_read_main(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


def test_redirect(test_client):
    response = test_client.get("/")
    assert response.request.path_url == "/docs"


def test_insert_items(test_client, test_items):
    response = test_client.post("/api/v1/col/item", json=test_items)
    assert response.status_code == 201


def test_insert_user(test_client, test_user):
    response = test_client.post("/api/v1/col/user", json=test_user)
    assert response.status_code == 201


def test_insert_recommendations(test_client, test_recommendations_ib_cf):
    print("Implement test")


def test_ab_testing_with_reco_js_cookie(test_client):
    res = test_client.get("/api/v1/rec/testing/ab?test_name=ab_test&item_id_seed=123",
                          cookies={cfg.RECO_JS_COOKIE_ID: "cookie_test"})
    assert res.json() == 'cookie_test'


def test_ab_testing_without_reco_js_cookie(test_client):
    res = test_client.get("/api/v1/rec/testing/ab?test_name=mytest&item_id_seed=123")
    assert res.json() is None
