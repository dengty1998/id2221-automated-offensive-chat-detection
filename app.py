from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
from datetime import datetime
from Connectors.cassandra_connector import check_password
from Connectors.kafka_producer import flush_message
from Connectors.redis_connector import return_parsed_data
from utils.word_checker import check_word


app = Flask(__name__)
app.secret_key = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# kafka_consumer_thread = Thread(target=kafka_consumer.consumer_message("chatlogs"))
# kafka_consumer_thread.daemon = True
# kafka_consumer_thread.start()
# executor = ThreadPoolExecutor(max_workers=1)
# future = executor.submit(kafka_consumer.consumer_message("chatlogs"))





class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user


@app.route('/')
def index():
    return redirect(url_for('login'))
    # if current_user.is_authenticated:
    #     return redirect(url_for('dashboard'))
    # else:
    #     return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_password(username, password):
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

    # contain_offensive_language = False
    # if "fuck" in message['msg']:
    #     contain_offensive_language = True
    contain_offensive_language = check_word(message['msg'])

    emit('contain_offensive_language', {'value': contain_offensive_language})


    current_datetime = datetime.now()
    timestamp = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    json_text = {
        'username': str(message['username']),
        'message': str(message['msg']),
        'timestamp': str(timestamp),
    }

    #flush_message('chatlogs', message['msg'])
    flush_message('chatlogs', json.dumps(json_text))


@socketio.on('left', namespace='/chat')
@login_required
def left(message):
    room = message['room']
    leave_room(room)
    send({'msg': message['username'] + " leave the channel."}, room=room)


@socketio.on("reportUser", namespace="/chat")
@login_required
def report_user(message):
    reported_username = message.get("reportedUsername")
    data_list = return_parsed_data()
    message_list = []
    for data in data_list:
        if data["username"] == reported_username:
            message_list.append(data)
    return_message = str(message_list[-3:])

    emit("receiveReport", {'name': reported_username, 'message': return_message}, broadcast=True)


# change network profile from public to private then replace host argument with server's ip
if __name__ == '__main__':

    socketio.run(app, host='192.168.199.128', port=5001,
                 debug=True, allow_unsafe_werkzeug=True)


