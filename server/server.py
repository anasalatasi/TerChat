from flask import Flask, jsonify, request
from datetime import datetime
from db_service import DatabaseService
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

# Request handlers
@app.route('/messages', methods=['POST'])
def send_message():
    data = request.get_json()
    if not data or 'text' not in data:
        raise BadRequest("Missing 'text' in request body")
    
    message = {
        'text': data['text'],
        'timestamp': datetime.now().isoformat(),
        'sender': data.get('sender', 'unknown')
    }
    DatabaseService.insert_message(message['text'], message['timestamp'], message['sender'])
    return jsonify({'status': 'Message received'}), 200

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = DatabaseService.get_all_messages()
    return jsonify(messages), 200

@app.route('/messages/count', methods=['GET'])
def message_count():
    count = DatabaseService.get_message_count()
    return jsonify({'count': count}), 200

def run_server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    DatabaseService.init_db()
    run_server()
