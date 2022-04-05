from flask_restx import Resource
from flask_jwt import jwt_required

from .scraper import get_articles


class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello World"}


class ArticleList(Resource):
    def get(self):
        return get_articles()


class Article(Resource):
    @jwt_required()
    def get(self, index):
        articles = get_articles()
        if index >= len(articles) + 1:
            return {"message": "Article index out of range"}
        return articles[index - 1]
