from requests.auth import HTTPBasicAuth
import api.core.util.config as cfg


class TestRecommendationAPI:
    # BUILDER

    def test_ib_cf_builder(self, test_client, test_evidence):
        res = test_client.put("/api/v1/bld", auth=HTTPBasicAuth('admin', 'nimda'))
        assert res.status_code == 201

    # SPLITTING CONFIG

    def test_insert_splitting(self, test_client, test_splitting1, test_splitting2):
        res = test_client.post("/api/v1/rec/split/config?name=split1", json=test_splitting1,
                               auth=HTTPBasicAuth('admin', 'nimda'))
        assert res.status_code == 200
        res = test_client.post("/api/v1/rec/split/config?name=split2", json=test_splitting2,
                               auth=HTTPBasicAuth('admin', 'nimda'))
        assert res.status_code == 200

    def test_get_splitting(self, test_client, test_splitting1):
        res = test_client.get("/api/v1/rec/split/config?name=split1", auth=HTTPBasicAuth('admin', 'nimda'))
        assert res.json()["methods"] == test_splitting1

    # SPLIT RECOS

    def test_splitting_assigned_user(self, test_client):
        res = test_client.get("/api/v1/rec/split?name=split1&item_id_seed=419",
                              cookies={cfg.RECO_COOKIE_ID: "petes_cookie"})
        assert len(res.json()) == 5

    def test_splitting_unassigned_user(self, test_client):
        res = test_client.get("/api/v1/rec/split?name=split2&item_id_seed=419",
                              cookies={cfg.RECO_COOKIE_ID: "petes_cookie"})
        assert len(res.json()) == 5

    def test_splitting_new_user(self, test_client):
        res = test_client.get("/api/v1/rec/split?name=split11&item_id_seed=1",
                              cookies={cfg.RECO_COOKIE_ID: "andres_cookie"})
        assert len(res.json()) == 5
