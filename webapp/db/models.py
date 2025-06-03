from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from webapp.db import db
from flask_login import UserMixin, current_user


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=False)

    
class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    reciever_id = db.Column(db.Integer)
    status = db.Column(db.String, nullable=False)

    

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    text = db.Column(db.String(32), nullable=False)
    #chat_id = db.Column(db.Integer)