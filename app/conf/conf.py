class Config(object):
   DEBUG = False
   TESTING = False
   SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
   SQLALCHEMY_DATABASE_URI = "mysql+pymysql://setiadi:123456@127.0.0.1:3306/db_api_2"
   SQLALCHEMY_ECHO = False
   JWT_SECRET_KEY = 'JWT-SECRET'
   SECRET_KEY = 'SECRET-KEY'
   SECURITY_PASSWORD_SALT = 'SECRET-KEY-PASSWORD'
   MAIL_DEFAULT_SENDER = 'wanlunxin@gmail.com'
   MAIL_SERVER = 'smtp.gmail.com'
   MAIL_PORT = '465'
   MAIL_USERNAME = 'wanlunxin@gmail.com'
   MAIL_PASSWORD = 'confirmeddna0'
   MAIL_USE_TLS = False
   MAIL_USE_SSL = True
   UPLOAD_FOLDER = 'app/static/images/avatars'


class DevelopmentConfig(Config):
   DEBUG = True
   SQLALCHEMY_DATABASE_URI = "mysql+pymysql://setiadi:123456@127.0.0.1:3306/db_api_2"
   SQLALCHEMY_ECHO = False
   JWT_SECRET_KEY = 'JWT-SECRET'
   SECRET_KEY = 'SECRET-KEY'
   SECURITY_PASSWORD_SALT = 'SECRET-KEY-PASSWORD'
   MAIL_DEFAULT_SENDER = 'wanlunxin@gmail.com'
   MAIL_SERVER = 'smtp.gmail.com'
   MAIL_PORT = '465'
   MAIL_USERNAME = 'wanlunxin@gmail.com'
   MAIL_PASSWORD = 'confirmeddna0'
   MAIL_USE_TLS = False
   MAIL_USE_SSL = True
   UPLOAD_FOLDER = 'app/static/images/avatars'


class TestingConfig(Config):
   TESTING = True
   SQLALCHEMY_DATABASE_URI = "mysql+pymysql://setiadi:123456@127.0.0.1:3306/db_api_2"
   SQLALCHEMY_ECHO = False
   JWT_SECRET_KEY = 'JWT-SECRET'
   SECRET_KEY = 'SECRET-KEY'
   SECURITY_PASSWORD_SALT = 'SECRET-KEY-PASSWORD'
   MAIL_DEFAULT_SENDER = 'wanlunxin@gmail.com'
   MAIL_SERVER = 'smtp.gmail.com'
   MAIL_PORT = '465'
   MAIL_USERNAME = 'wanlunxin@gmail.com'
   MAIL_PASSWORD = 'confirmeddna0'
   MAIL_USE_TLS = False
   MAIL_USE_SSL = True
   UPLOAD_FOLDER = 'app/static/images/avatars'
