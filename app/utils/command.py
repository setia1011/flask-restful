from flask import Blueprint
from app.models.user import db as db_user
from app.models.author import db as db_author
from app.models.book import db as db_book


cmd = Blueprint('cmd', __name__)

@cmd.cli.command('init')
def init():
    db_user.create_all()
    print("tbl_user created")
    db_author.create_all()
    print("tbl_author created")
    db_book.create_all()
    print("tbl_book created")

@cmd.cli.command('drop')
def drop():
    db_user.drop_all()
    print("tbl_user dropped")
    db_book.drop_all()
    print("tbl_book dropped")
    db_author.drop_all()
    print("tbl_author dropped")



