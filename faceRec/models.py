from flask_sqlalchemy import SQLAlchemy
from .views import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    profile_picture = db.Column(db.String(255), nullable=False)
