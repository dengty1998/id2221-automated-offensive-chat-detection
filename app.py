from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
from datetime import datetime
import fileinput

app = Flask(__name__)
app.secret_key = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

users = {'dty': {'password': '123456'}, 'amy': {'password': '654321'}}


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return 'Login failed. Please check your credentials.'

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    username = current_user.get_id()
    return render_template('index.html', username=username)


@socketio.on('join', namespace='/chat')
@login_required
def join(message):
    room = message['room']
    join_room(room)
    send({'msg': message['username'] + " join the " +
         message['room'] + " channel."}, room=room)


@socketio.on('text', namespace='/chat')
@login_required
def text(message):
    room = message['room']
    send({'msg': message['username'] + "[" +
         message['room'] + "]: " + message['msg']}, room=room)

    current_datetime = datetime.now()
    timestamp = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    json_text = {
        'username': str(message['username']),
        'message': str(message['msg']),
        'timestamp': str(timestamp),
    }

    json_file_path = "D:/Workspace/ID2221/generated.json"


@socketio.on('left', namespace='/chat')
@login_required
def left(message):
    room = message['room']
    leave_room(room)
    send({'msg': message['username'] + " leave the channel."}, room=room)


# change network profile from public to private then replace host argument with server's ip
if __name__ == '__main__':
    socketio.run(app,  # host = '130.229.130.154', port = 5000,
                 debug=True, allow_unsafe_werkzeug=True)
