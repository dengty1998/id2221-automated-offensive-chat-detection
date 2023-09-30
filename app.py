from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.secret_key = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('join', namespace='/chat')
def join(message):
    room = message['room']
    join_room(room)
    send({'msg': message['username'] + " join the " +
         message['room'] + " channel."}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = message['room']
    send({'msg': message['username'] + "[" +
         message['room'] + "]: " + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = message['room']
    leave_room(room)
    send({'msg': message['username'] + " leave the channel."}, room=room)


# change network profile from public to private then replace host argument with server's ip
if __name__ == '__main__':
    socketio.run(app,  # host = '130.229.130.154', port = 5000,
                 debug=True, allow_unsafe_werkzeug=True)
