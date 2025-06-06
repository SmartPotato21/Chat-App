from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from webapp.db import db
from flask_login import UserMixin, current_user


# User model for authentication and user data
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String, unique=True)  # Username (must be unique)
    password = db.Column(db.String, unique=False) # User's password (should be hashed in production)

# Friend model to represent friend relationships and requests
class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)      # Unique ID for the friend relationship
    sender_id = db.Column(db.Integer)                 # User ID of the sender
    reciever_id = db.Column(db.Integer)               # User ID of the receiver
    status = db.Column(db.String, nullable=False)     # Status of the friendship (e.g., 'pending', 'accepted')

# Message model for storing chat messages
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)      # Unique message ID
    sender_id = db.Column(db.Integer)                 # User ID of the sender
    receiver_id = db.Column(db.Integer)               # User ID of the receiver
    text = db.Column(db.String(32), nullable=False)   # Message text (max 32 characters)
    #chat_id = db.Column(db.Integer)                  # (Optional) Chat ID for group chats or threads