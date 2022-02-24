from api.core.services.builder.CollaborativeFilteringBuilder import CollaborativeFilteringBuilder
import api.core.util.config as cfg


def test_insert_relations(test_client, test_relations_ib_cf):
    cfb = CollaborativeFilteringBuilder(df=None)
    cfb.relations = test_relations_ib_cf
    cfb.store_relations()


def test_splitting_assigned_user(test_client):
    res = test_client.get("/api/v1/rec/split?name=split1&item_id_seed=1",
                          cookies={cfg.RECO_COOKIE_ID: "petes_cookie"})
    assert len(res.json()) == 5


def test_splitting_unassigned_user(test_client):
    res = test_client.get("/api/v1/rec/split?name=split2&item_id_seed=1",
                          cookies={cfg.RECO_COOKIE_ID: "petes_cookie"})
    assert len(res.json()) == 5


def test_splitting_new_user(test_client):
    res = test_client.get("/api/v1/rec/split?name=split11&item_id_seed=1",
                          cookies={cfg.RECO_COOKIE_ID: "andres_cookie"})
    assert len(res.json()) == 5
