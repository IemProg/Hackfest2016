from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)



@app.route('/')
def index():
    return 'This is the backend'

@socketio.on('connect')
def connect():
    # train model
    emit('Client connected', {'data': 'Connected'})


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('photo')
def dealWithPhoto(photo):
    print photo
    emit('my response', {'data': 'got it!'})

if __name__ == '__main__':
    socketio.run(app, port=33507)
