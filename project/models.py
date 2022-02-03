from enum import unique
from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    about = db.Column(db.String(10000))


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    title = db.Column(db.String(1000))
    description = db.Column(db.String(2000))

    def __init__(self, file_name, category, title, description) -> None:
        super().__init__()
        self.file_name = file_name
        self.category = category
        self.title = title
        self.description = description
