from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from webapp import app
import bcrypt

from webapp.db import db
from webapp.db.models import User
from webapp.db.manage import addUser




@app.route("/")
def home():

    

    return "home"


@app.route("/login", methods = ['GET','POST'])
def login_page():
    active_tab = '1'

    if request.method == 'POST':
        if 'login_page_select' in request.form:
            active_tab = '1'
        if 'register_page_select' in request.form:
            active_tab = '2'
            
        if 'register_submit' in request.form:
            username = request.form.get("username")
            password = request.form.get("password")
        
            found_user = User.query.filter_by(username=username).first()
            if(found_user):
                return "Username exists"
            
            addUser(username,password)
            print("new user added")
            
        if 'login_submit' in request.form:
            
            
            username = request.form.get("username")
            password = request.form.get("password")
            
            found_user = User.query.filter_by(username=username).first()
            if not found_user:
                return "User not found"
            
            userBytes = password.encode('utf-8')
            result = bcrypt.checkpw(userBytes, found_user.password.encode('utf-8'))
            
            if result:
                return render_template('chat.html', username=username)
            else:
                return "Incorrect password"
            
    
        
    return render_template('login.html',show = active_tab)


@app.route("/chat")
def chat_page():


    return "in chat"