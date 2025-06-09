from webapp.db import db
from webapp import app
import bcrypt
from webapp.db.models import User, Message, Friend
from flask_socketio import SocketIO, emit


def User_addUser(username,password):
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
        from webapp.db.models import User, Message, Friend

        db.create_all()
        
def User_remove(username):
    with app.app_context():
        User.query.filter_by(username=username).delete()
        db.session.commit()


def Message_dropAll():      
    with app.app_context():
        # Drop the Message table from the database
        Message.__table__.drop(db.engine)

        # If you want to also remove it from SQLAlchemy's metadata:
        db.metadata.remove(Message.__table__)

def Message_addMessage(receiver_id, sender_id, message, sender_name):
    with app.app_context():
        new_message = Message(sender_id=sender_id, text=message, receiver_id=receiver_id)
        db.session.add(new_message)
        db.session.commit()
        
        from webapp.main import socketio
        
        
        # socketio.emit(
        #     'message_sent',
        #     {'receiver_id': receiver_id, 'text': message, 'own': True},
        #     room=f"user_{sender_id}"
        # )
        

        # Notify receiver
        socketio.emit(
            'message_sent',
            {'sender_id': sender_id, 'text': message, 'own': False, 'sender_name': sender_name},
            room=f"user_{receiver_id}"
        )
    
def Friends_addFriend(sender_id, reciever_id, status="pending"):
    with app.app_context():
        ship = Friend.query.filter_by(sender_id=reciever_id, reciever_id=sender_id).first()
        if ship:
            if ship.status == "pending":
                ship.status = "accepted"
                db.session.commit()    
                
                sender_username = User.query.get(sender_id).username
                reciever_username = User.query.get(reciever_id).username
                
                from webapp.main import socketio


                socketio.emit(
                    'friend_accepted',
                    {'friend':{'id': reciever_id, 'username': reciever_username}},
                    room=f"user_{sender_id}"
                )
                print(f"Emitted to user_{sender_id}")
    
                # Notify receiver (the one who accepted)
                socketio.emit(
                    'friend_accepted',
                    {'friend':{'id': sender_id, 'username': sender_username}},
                    room=f"user_{reciever_id}"
                )
                print(f"Emitted to user_{reciever_id}")

                
                return;      
        else:
            new_friend = Friend(sender_id=sender_id, reciever_id=reciever_id, status=status)
            db.session.add(new_friend)
            db.session.commit()
            sender_username = User.query.get(sender_id).username
            print(f"Added friend request from {sender_username} to {reciever_id}")
            
            from webapp.main import socketio

            socketio.emit(
                    'mail_sent',
                    {'sender_username': sender_username },
                    room=f"user_{reciever_id}"
                )
            
def Friend_dropAll(password):
    if password == "q1q1q1":
        with app.app_context():
            db.metadata.drop_all(bind=db.engine, tables=[Friend.__table__])

                        
            
            
