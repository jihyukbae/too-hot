from app import app
from flask_socketio import SocketIO

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)
socketio.run(app)