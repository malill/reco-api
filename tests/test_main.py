from starlette.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_redirect():
    response = client.get("/")
    assert response.request.path_url == "/docs"
