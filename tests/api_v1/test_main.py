def test_read_main(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


def test_redirect(test_client):
    response = test_client.get("/")
    assert response.request.path_url == "/docs"
