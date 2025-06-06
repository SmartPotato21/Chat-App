from flask import Flask, request, redirect, url_for, render_template, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room

from webapp import app

import bcrypt

from webapp.db import db
from webapp.db.models import User
from webapp.db.manage import *


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)


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
            
            User_addUser(username,password)
          
            
        if 'login_submit' in request.form:
            
            
            username = request.form.get("username")
            password = request.form.get("password")
            confirmpassword = request.form.get("confirm-password")
            
            

                    
            found_user = User.query.filter_by(username=username).first()
            if not found_user:
                return "User not found"
            
            session['username'] = username
            session['user_id'] = found_user.id
            session['password'] = password
            
            
            
            userBytes = password.encode('utf-8')
            result = bcrypt.checkpw(userBytes, found_user.password.encode('utf-8'))
            
            if result:
                
                login_user(found_user)
                
                
                return redirect('/chat')
            else:
                return "Incorrect password"
            
    
        
    return render_template('login.html',show = active_tab)


# Handle chat page logic, including friend list, message sending, and adding friends
@app.route("/chat",methods = ['GET','POST'])
@login_required
def chat_page():
    print(current_user.is_authenticated)
    if not current_user.is_authenticated:
        return redirect('/login')
    
    # Load current user's friends and requests
    friend_list, request_list = load_friends()
    current_chat = None

    # Handle POST requests for logout, sending messages, and adding friends
    if request.method == 'POST':
        # Handle logout
        if 'logout_select' in request.form:
            return redirect('/logout')
        # Handle sending a message
        if 'message-submit' in request.form:
            print(request.form.get("receiver"))
            print("sender", request.form.get("sender"))
            receiver_id = User.query.filter_by(username=request.form.get("receiver")).first().id
            message = request.form.get("message")
            if message:
                # Add message to database
                Message_addMessage(receiver_id, current_user.id, message, request.form.get("sender"))
                return jsonify({
                    'success': True,
                    'message': 'Message sent successfully!'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Message cannot be empty.'
                })
        # Handle adding a friend
        if 'add-friend' in request.form:
            friend_username = request.form.get("friend-username")
            if friend_username and friend_username != current_user.username:
                friend = User.query.filter_by(username=friend_username).first()
                if friend:
                    # Check if already friends
                    existing_friendship = Friend.query.filter(
                        ((Friend.sender_id == current_user.id) & (Friend.reciever_id == friend.id)) |
                        ((Friend.reciever_id == friend.id) & (Friend.sender_id == current_user.id))
                    ).first()
                    
                    if existing_friendship:
                        return jsonify({
                            'success': False,
                            'message': 'You are already friends with this user.'
                        })
                    
                    # Add new friend relationship
                    Friends_addFriend(current_user.id, friend.id)
                    return jsonify({
                        'success': True,
                        'message': 'Friend added successfully!',
                        'friend': {
                            'id': friend.id,
                            'username': friend.username
                        }
                    })
            elif friend_username == current_user.username:                
                # Prevent adding yourself as a friend
                socketio.emit(
                    'add-friend-error',
                    {'error': "Cant add yourself as a friend!"}
                )
                return jsonify(success=False, error='Something went wrong')
    # Render chat page with user info and messages
    return render_template('chat.html', username = current_user.username, friend_list= friend_list, messages=getMessages())


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


def load_friends():
    if not current_user.is_authenticated:
        return []
    
    friends = Friend.query.filter((Friend.sender_id == current_user.id) | (Friend.reciever_id == current_user.id)).all()
    friend_list = []
    request_list = []
    
    for friend in friends:
        if friend.status == "accepted":
            if friend.sender_id == current_user.id:
                to_add = localFriend(id=friend.reciever_id,username=User.query.get(friend.reciever_id).username)
                friend_list.append(to_add)
            else:
                to_add = localFriend(id=friend.sender_id,username=User.query.get(friend.sender_id).username)
                friend_list.append(to_add)
        else:
            to_add = localFriend(id=friend.sender_id,username=User.query.get(friend.sender_id).username)

            request_list.append(to_add)
    
    return (friend_list, request_list)

    

class localFriend:
    id = 0
    username = "blank"
    def __init__(self, id, username):
        self.id = id
        self.username = username
        
        
def getMessages():
    if not current_user.is_authenticated:
        return []
    
    messages = Message.query.filter_by(sender_id=current_user.id).all()
    return messages



@app.route('/get_messages', methods=['POST'])
def get_messages():
    print("dsada")
    
    friend_username = request.form.get('friend')

    friend = User.query.filter_by(username=friend_username).first()
    if not friend:
        return jsonify({'success': False, 'error': 'Friend not found'})

    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == friend.id)) |
        ((Message.sender_id == friend.id) & (Message.receiver_id == current_user.id))
    )

    # Serialize messages
    message_list = [
        {
            'sender': msg.sender_id,
            'text': msg.text,
            'is_own': msg.sender_id == current_user.id
        }  for msg in messages
        
        
    ]
    for msg in message_list:
        print("Message: ",msg['text'])
    return jsonify({'success': True, 'messages': message_list})


        
        
@socketio.on('connect')
def on_connect():

    
    if current_user.is_authenticated:
        user_id = current_user.id
        username = current_user.username
        room_name = f'user_{user_id}'
        join_room(room_name)

