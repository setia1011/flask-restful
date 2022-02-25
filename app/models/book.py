from app.utils.database import db
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields


class Book(db.Model):
   __tablename__ = 'tbl_book'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   title = db.Column(db.String(100))
   year = db.Column(db.Integer)
   author_id = db.Column(db.Integer, db.ForeignKey('tbl_author.id'), nullable=False)

   def __init__(self, title, year, author_id=None):
      self.title = title
      self.year = year
      self.author_id = author_id

   def create(self):
      db.session.add(self)
      db.session.commit()
      return self


class BookSchema(SQLAlchemySchema):
   class Meta(SQLAlchemySchema.Meta):
      model = Book
      sqla_session = db.session
      load_instance = True

   id = fields.Number(dump_only=True)
   title = fields.String(required=True)
   year = fields.Integer(required=True)
   author_id = fields.Integer()
