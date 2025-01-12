from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins


@app.route('/webhook', methods=['POST'])
def webhook():
    alert = request.json
    print("Received alert:", alert)
    socketio.emit('alert', alert)
    return '', 200

@app.route('/webhook/volume', methods=['POST'])
def webhook_volume():
    volume_data = request.json
    print("Volume control:", volume_data)
    socketio.emit('volume', volume_data)
    return '', 200

@app.route('/webhook/screamer', methods=['POST'])
def webhook_screamer():
    print("Screamer triggered")
    socketio.emit('screamer', {"message": "Screamer activated!"})
    return '', 200

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.after_request
def apply_cors(response):
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
    return response


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3001)
