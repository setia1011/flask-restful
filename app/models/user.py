from app.utils.database import db
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields
from passlib.hash import pbkdf2_sha256 as sha256


class User(db.Model):
    __tablename__ = 'tbl_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    nickname = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    verified = db.Column(db.Enum('0', '1'), nullable=False, server_default='0')

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_hoo(cls, hoo):
        return cls.query.filter_by(hoo=hoo).first

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_fullname(cls, fullname):
        return cls.query.filter_by(fullname=fullname).first()

    @classmethod
    def find_by_nickname(cls, nickname):
        return cls.query.filter_by(nickname=nickname).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class UserSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = User
        sqla_session = db.session
        load_instance = True

    id = fields.Number(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    fullname = fields.String(required=True)
    nickname = fields.String(required=True)
    email = fields.String(required=True)

