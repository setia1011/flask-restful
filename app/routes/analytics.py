from flask import Blueprint
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.database import db

from app.models.book import Book
from app.models.author import Author


analytics_routes = Blueprint('analytics', __name__)


@analytics_routes.route("", methods=['GET'], endpoint='index')
def index():
   books = Book.query.all()
   li = []
   for i in books:
      li.append({
         "book_id": i.id,
         "title": i.title,
         "year": i.year,
         "author_id": i.author_id
      })
   return response_with(resp.SUCCESS_200, value={"data": li})

@analytics_routes.route("/books", methods=['GET'], endpoint='books')
def books():
   books = db.session.query(Book, Author).filter(Book.author_id == Author.id).all()
   li = []
   for i, j in books:
      li.append({
         "book_id": i.id,
         "title": i.title,
         "year": i.year,
         "author_id": i.author_id,
         "author_first_name": j.first_name,
         "author_last_name": j.last_name
      })
   return response_with(resp.SUCCESS_200, value={"data": li})