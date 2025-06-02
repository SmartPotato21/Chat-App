from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from db import db
from db.models import User


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'db', 'users.db')}"
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():

    user = User(username="y")
    db.session.add(user)
    db.session.commit()

    return "home"


@app.route("/login", methods = ['GET','POST'])
def login_page():
    active_tab = '1'



    if request.method == 'POST':
        if 'login_page_select' in request.form:
            active_tab = '1'
        if 'register_page_select' in request.form:
            active_tab = '2'
    
        
    return render_template('login.html',show = active_tab)


@app.route("/chat")
def chat_page():


    return "in chat"