from flask import Flask, render_template,request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    name = data['name']
    print(f'{name} joined the chat.')
    socketio.emit('message', {'name': 'System', 'message': f'{name} joined the chat.'})

@socketio.on('message')
def handle_message(data):
    # client_id = request.sid
    name = data['name']
    message = data['message']
    print(f'{name}: {message}')
    socketio.emit('message', {'name': name, 'message': message})
    
# @socketio.on('message')
# def handle_message(msg):
#     print('Message:', msg)
#     socketio.emit('message', msg)

if __name__ == '__main__':
    socketio.run(app, debug=True)
