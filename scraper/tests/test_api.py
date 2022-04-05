from scraper import app


def test_hello_world():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert response.json["message"] == "Hello World"


def test_failed_article_list():
    response = app.test_client().get("/articles")

    assert response.status_code == 500
    # assert response.json["error"] == "Authorization Required"
