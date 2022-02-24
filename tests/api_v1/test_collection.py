from requests.auth import HTTPBasicAuth


def test_insert_user(test_client, test_user):
    response = test_client.post("/api/v1/col/user", json=test_user, auth=HTTPBasicAuth('admin', 'nimda'))
    assert response.json()["first_name"] == "Pete"


def test_get_user_existing(test_client):
    response = test_client.get("/api/v1/col/user?cookie_value=petes_cookie", auth=HTTPBasicAuth('admin', 'nimda'))
    assert response.json()["first_name"] == "Pete"


def test_get_user_new(test_client):
    response = test_client.get("/api/v1/col/user?cookie_value=steffis_cookie", auth=HTTPBasicAuth('admin', 'nimda'))
    assert "steffis_cookie" in response.json()["keys"]["cookie"]


def test_insert_items(test_client, test_product_items):
    response = test_client.post("/api/v1/col/item", json=test_product_items, auth=HTTPBasicAuth('admin', 'nimda'))
    assert response.status_code == 201
