from flask import Flask, render_template
import os
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
    print 'Connected!'
    emit('Client connected', {'data': 'Connected'})


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('photo')
def dealWithPhoto(photo):
    print photo
    emit('my response', {'data': 'got it!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print port
    socketio.run(app, port=port)
