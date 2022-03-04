from requests.auth import HTTPBasicAuth
import api.core.util.config as cfg


class TestCollectionAPI:
    # EVIDENCE
    def test_insert_evidence(self, test_client, test_evidence):
        response = test_client.put("/api/v1/col/evidence", json=test_evidence, headers={"reco-user-uid": "external"})
        assert response.json() == len(test_evidence)

    # ITEMS
    def test_insert_items(self, test_client, test_items):
        response = test_client.post("/api/v1/col/item", json=test_items, auth=HTTPBasicAuth('admin', 'nimda'))
        assert response.status_code == 201

    def test_get_all_items(self, test_client, test_items):
        response = test_client.get("/api/v1/col/item/all", auth=HTTPBasicAuth('admin', 'nimda'))
        assert len(response.json()) == len(test_items)

    def test_get_item_by_id(self, test_client):
        item_id = str(415)
        response = test_client.get(f"/api/v1/col/item?item_id={item_id}", auth=HTTPBasicAuth('admin', 'nimda'))
        assert response.json()["id"] == item_id

    def test_delete_item(self, test_client):
        response = test_client.delete("/api/v1/col/item?item_id=419", auth=HTTPBasicAuth('admin', 'nimda'))
        assert response.json() == 1

    # USER
    def test_post_new_user(self, test_client, test_user1):
        response = test_client.post("/api/v1/col/user",
                                    headers={cfg.RECO2JS_ID: "petes_reco2js_id"},
                                    json=test_user1,
                                    auth=HTTPBasicAuth('admin', 'nimda'))
        assert response.status_code == 200

    def test_get_existing_user(self, test_client):
        response = test_client.get("/api/v1/col/user/id?reco2js_id=petes_reco2js_id",
                                   auth=HTTPBasicAuth('admin', 'nimda'))
        assert response.json()["first_name"] == "Pete"

    def test_delete_user_by_cookie(self, test_client):
        response = test_client.delete("/api/v1/col/user?reco2js_id=petes_reco2js_id",
                                      auth=HTTPBasicAuth('admin', 'nimda'))
        assert response.json() == 1
