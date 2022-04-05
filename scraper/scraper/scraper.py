import requests
from bs4 import BeautifulSoup

URL = "https://www.politifact.com/factchecks/list/"


def get_articles():
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html5lib")
        results = soup.find(class_="o-listicle__list")
        articles = results.find_all("li", class_="o-listicle__item")
        content = []
        for article in articles:
            content.append(
                {
                    "heading": article.find(
                        "div", class_="m-statement__quote"
                    ).text.strip(),
                    "link": article.find("a")["href"],
                }
            )
        return content
    except Exception as e:
        print(e)
