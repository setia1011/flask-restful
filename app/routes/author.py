from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
import os

from werkzeug.utils import secure_filename

from app.models.author import AuthorSchema, Author
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.database import db
from app.utils.useful import random_string

author_routes = Blueprint("author_routes", __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@author_routes.route('', methods=['POST'], endpoint='create_author')
# @jwt_required
def create_author():
   try:
      data = request.get_json()
      author_schema = AuthorSchema()
      author = author_schema.load(data)
      result = author_schema.dump(author.create())
      return response_with(resp.SUCCESS_201, value={"author": result})
   except Exception as e:
      return response_with(resp.INVALID_INPUT_422)


@author_routes.route('/avatar/<int:author_id>', methods=['POST'], endpoint='upsert_author_avatar')
# @jwt_required
def upsert_author_avatar(author_id):
   try:
      file = request.files['avatar']
      get_author = Author.query.get_or_404(author_id)
      filePath = current_app.config['UPLOAD_FOLDER']
      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         filenamex = 'aUtHor' + str(author_id) + '_' + random_string(16) + '.' + filename.split('.')[1]
         file.save(os.path.join(filePath, filenamex))
         if get_author.avatar is not None:
            if os.path.exists(os.path.join(filePath, get_author.avatar)):
               os.unlink(os.path.join(filePath, get_author.avatar))
         else:
            print("Can't delete the file as it doesn't exists")
         get_author.avatar = filenamex
         db.session.add(get_author)
         db.session.commit()
         author_schema = AuthorSchema()
         author = author_schema.dump(get_author)
         return response_with(resp.SUCCESS_200, value={"author": author})
      else:
         return response_with(resp.INVALID_INPUT_422)
   except Exception as e:
      print(e)
      return response_with(resp.INVALID_INPUT_422)


@author_routes.route('', methods=['GET'], endpoint='get_author_list')
def get_author_list():
   fetched = Author.query.all()
   author_schema = AuthorSchema(many=True, only=['id','first_name','last_name','avatar','created'])
   authors = author_schema.dump(fetched)
   return response_with(resp.SUCCESS_200, value={"authors": authors})


@author_routes.route('/<int:author_id>', methods=['GET'], endpoint='get_author_detail')
def get_author_detail(author_id):
   fetched = Author.query.get_or_404(author_id)
   author_schema = AuthorSchema()
   author = author_schema.dump(fetched)
   return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:id>', methods=['PUT'], endpoint='update_author_detail')
# @jwt_required
def update_author_detail(id):
   data = request.get_json()
   get_author = Author.query.get_or_404(id)
   get_author.first_name = data['first_name']
   get_author.last_name = data['last_name']
   db.session.add(get_author)
   db.session.commit()
   author_schema = AuthorSchema()
   author = author_schema.dump(get_author)
   return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:id>', methods=['PATCH'], endpoint='modify_author_detail')
def modify_author_detail(id):
   data = request.get_json()
   get_author = Author.query.get(id)
   if data.get('first_name'):
      get_author.first_name = data['first_name']
   if data.get('last_name'):
      get_author.last_name = data['last_name']
   db.session.add(get_author)
   db.session.commit()
   author_schema = AuthorSchema()
   author = author_schema.dump(get_author)
   return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:id>', methods=['DELETE'], endpoint='delete_author')
def delete_author(id):
   get_author = Author.query.get_or_404(id)
   db.session.delete(get_author)
   db.session.commit()
   return response_with(resp.SUCCESS_204)
