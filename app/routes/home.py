from flask import Blueprint
from flask_jwt_extended import jwt_required

home_routes = Blueprint('home_routes', __name__)


@home_routes.route('/')
def index():
   return {"info": "API server is running..!"}
