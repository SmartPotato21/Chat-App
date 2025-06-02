from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from webapp import app

db = SQLAlchemy()

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'db', 'users.db')}"
db.init_app(app)

with app.app_context():
    db.create_all()

print("db/__init__.py has been imported")
