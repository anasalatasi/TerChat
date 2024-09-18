from flask import Flask, jsonify, request
from datetime import datetime
import threading

app = Flask(__name__)

messages = []

@app.route('/messages', methods=['POST'])
def send_message():
    data = request.get_json()
    message = {
        'text': data['text'],
        'timestamp': datetime.now().isoformat(),
        'sender': data.get('sender', 'unknown')
    }
    messages.append(message)
    return jsonify({'status': 'Message received'}), 200

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(messages), 200

@app.route('/messages/count', methods=['GET'])
def message_count():
    return jsonify({'count': len(messages)}), 200

def run_server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
