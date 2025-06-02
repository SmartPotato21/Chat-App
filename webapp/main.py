from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

from webapp import app

import bcrypt

from webapp.db import db
from webapp.db.models import User
from webapp.db.manage import addUser


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'


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
            
            session['username'] = username
            session['password'] = password
            
            print(found_user.id)
            
            userBytes = password.encode('utf-8')
            result = bcrypt.checkpw(userBytes, found_user.password.encode('utf-8'))
            
            if result:
                
                login_user(found_user)
                print("User logged in")
                
                return redirect('/chat')
            else:
                return "Incorrect password"
            
    
        
    return render_template('login.html',show = active_tab)


@app.route("/chat",methods = ['GET','POST'])
@login_required
def chat_page():
    print(current_user.is_authenticated)
    if not current_user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        if 'logout_select' in request.form:
            return redirect('/logout')
        
            

    return render_template('chat.html', username = current_user.username)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def logout_user():
    
    if '_fresh' in session:
        session.pop('_fresh')
    
        
        
        
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect("/login")