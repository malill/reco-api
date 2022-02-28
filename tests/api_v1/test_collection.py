from requests.auth import HTTPBasicAuth


class TestCollectionAPI:
    # EVIDENCE
    def test_insert_evidence(self, test_client, test_evidence):
        response = test_client.put("/api/v1/col/evidence", json=test_evidence)
        assert response.json() == len(test_evidence)

    # ITEMS
    def test_insert_items(self, test_client, test_items):
        response = test_client.post("/api/v1/col/item", json=test_items, auth=HTTPBasicAuth('admin', 'nimda'))
        assert response.status_code == 201

    def test_get_all_items(self, test_client, test_items):
        response = test_client.get("/api/v1/col/item", auth=HTTPBasicAuth('admin', 'nimda'))
        assert len(response.json()) == len(test_items)

    def test_delete_item(self, test_client):
        response = test_client.delete("/api/v1/col/item?item_id=419", auth=HTTPBasicAuth('admin', 'nimda'))
        assert response.json() == 1

    # USER
    def test_post_user(self, test_client, test_user1):
        response = test_client.post("/api/v1/col/user", json=test_user1, auth=HTTPBasicAuth('admin', 'nimda'))
        assert response.json()["first_name"] == "Pete"

    def test_get_existing_user(self, test_client):
        response = test_client.get("/api/v1/col/user/id?cookie_value=petes_cookie", auth=HTTPBasicAuth('admin', 'nimda'))
        assert response.json()["first_name"] == "Pete"

    def test_get_or_create_user(self, test_client):
        response = test_client.get("/api/v1/col/user?cookie_value=steffis_cookie", auth=HTTPBasicAuth('admin', 'nimda'))
        assert response.status_code == 200

    def test_delete_user_by_cookie(self, test_client):
        response = test_client.delete("/api/v1/col/user?cookie_value=steffis_cookie",
                                      auth=HTTPBasicAuth('admin', 'nimda'))
        assert response.json() == 1
