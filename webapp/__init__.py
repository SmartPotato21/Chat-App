from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# Optionally, import your routes to bind them to the app
from webapp import main
