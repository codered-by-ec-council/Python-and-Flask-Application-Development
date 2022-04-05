from scraper.scraper import get_articles


def test_get_articles():
    articles = get_articles()

    assert isinstance(articles, list)
