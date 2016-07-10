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
    emit('Client connected', {'data': 'Connected'})


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('gotsPhoto')
def test_message(message):
    print message
    emit('my response', {'data': 'got it!'})

if __name__ == '__main__':
    socketio.run(app)
