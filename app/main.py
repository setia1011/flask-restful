import os
import logging
from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager

from app.conf.conf import ProductionConfig, DevelopmentConfig, TestingConfig
from app.utils.responses import response_with
from app.utils.command import cmd
from app.utils.database import db as dbx
from app.routes.home import home_routes
from app.routes.user import user_routes
from app.routes.book import book_routes
from app.routes.author import author_routes
from app.routes.analytics import analytics_routes
from app.routes.google_trends import google_trends_routes
from app.utils import responses as resp
from app.utils.mail import mail

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

if os.environ.get('FLASK_ENV') == 'production':
   conf = ProductionConfig
elif os.environ.get('FLASK_ENV') == 'development':
   conf = DevelopmentConfig
else:
   conf = TestingConfig

print(f" * Environment class mode: {conf}")
app.config.from_object(conf)


@app.route('/avatar/<filename>')
def uploaded_file(filename):
   return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.after_request
def add_header(response):
   return response


@app.errorhandler(400)
def bad_request(e):
   logging.error(e)
   return response_with(resp.BAD_REQUEST_400)


@app.errorhandler(500)
def server_error(e):
   logging.error(e)
   return response_with(resp.SERVER_ERROR_500)


@app.errorhandler(404)
def not_found(e):
   logging.error(e)
   return response_with(resp.SERVER_ERROR_404)


mail.init_app(app)
dbx.init_app(app)
jwt = JWTManager(app)

# Routing
app.register_blueprint(cmd)
app.register_blueprint(home_routes, url_prefix='/')
app.register_blueprint(user_routes, url_prefix='/v1/users')
app.register_blueprint(book_routes, url_prefix='/v1/books')
app.register_blueprint(author_routes, url_prefix='/v1/authors')
app.register_blueprint(analytics_routes, url_prefix='/v1/analytics')
app.register_blueprint(google_trends_routes, url_prefix='/v1/youtube-trends')

if __name__ == "__main__":
   app.run()
