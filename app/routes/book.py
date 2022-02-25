from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.models.book import BookSchema, Book
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.database import db

book_routes = Blueprint("book_routes", __name__)


@book_routes.route('', methods=['POST'], endpoint='create_book')
# @jwt_required
def create_book():
   try:
      data = request.get_json()
      book_schema = BookSchema()
      book = book_schema.load(data)
      result = book_schema.dump(book.create())
      return response_with(resp.SUCCESS_201, value={"book": result})
   except Exception as e:
      print(e)
      return response_with(resp.INVALID_INPUT_422)


@book_routes.route('', methods=['GET'], endpoint='get_book_list')
def get_book_list():
   fetched = Book.query.all()
   book_schema = BookSchema(many=True, only=['author_id', 'title', 'year'])
   books = book_schema.dump(fetched)
   return response_with(resp.SUCCESS_200, value={"books": books})


@book_routes.route('/<int:id>', methods=['GET'], endpoint='get_book_detail')
def get_book_detail(id):
   fetched = Book.query.get_or_404(id)
   book_schema = BookSchema()
   books = book_schema.dump(fetched)
   return response_with(resp.SUCCESS_200, value={"books": books})


@book_routes.route('/<int:id>', methods=['PUT'], endpoint='update_book_detail')
# @jwt_required
def update_book_detail(id):
   data = request.get_json()
   get_book = Book.query.get_or_404(id)
   get_book.title = data['title']
   get_book.year = data['year']
   db.session.add(get_book)
   db.session.commit()
   book_schema = BookSchema()
   book = book_schema.dump(get_book)
   return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route('/<int:id>', methods=['PATCH'], endpoint='modify_book_detail')
# @jwt_required
def modify_book_detail(id):
   data = request.get_json()
   get_book = Book.query.get_or_404(id)
   if data.get('title'):
      get_book.title = data['title']
   if data.get('year'):
      get_book.year = data['year']
   db.session.add(get_book)
   db.session.commit()
   book_schema = BookSchema()
   book = book_schema.dump(get_book)
   return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route('/<int:id>', methods=['DELETE'], endpoint='delete_book')
# @jwt_required
def delete_book(id):
   get_book = Book.query.get_or_404(id)
   db.session.delete(get_book)
   db.session.commit()
   return response_with(resp.SUCCESS_204)
