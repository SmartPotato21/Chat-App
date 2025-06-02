from webapp.db import db
from webapp import app
import bcrypt
from webapp.db.models import User

def addUser(username,password):
    with app.app_context():
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
    
        
        new_user  = User(username=username, password=hash.decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()

def dropAll(password):
    if password == "q1q1q1":
        with app.app_context():
            db.drop_all()
            
def createAll():
    with app.app_context():
        db.create_all()
        
def removeUser(username):
    with app.app_context():
        User.query.filter_by(username=username).delete()
        db.session.commit()
    