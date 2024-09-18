from flask import Flask, jsonify, request, Response
from datetime import datetime
from db_service import DatabaseService
from werkzeug.exceptions import BadRequest
from functools import lru_cache
from time import time
import json

app = Flask(__name__)

# SSE message queue
message_queue = []


# Caching
@lru_cache(maxsize=1)
def get_cached_message_count():
    return DatabaseService.get_message_count()

def clear_message_count_cache():
    get_cached_message_count.cache_clear()

# Clear cache every 2 seconds
@app.before_request
def clear_cache_periodically():
    if time() - clear_cache_periodically.last_clear > 2:
        clear_message_count_cache()
        clear_cache_periodically.last_clear = time()


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
    message_queue.append(message)
    return jsonify({'status': 'Message received'}), 200

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = DatabaseService.get_all_messages()
    return jsonify(messages), 200

@app.route('/messages/count', methods=['GET'])
def message_count():
    return jsonify({'count': get_cached_message_count()}), 200


@app.route('/stream')
def stream():
    def event_stream():
        while True:
            if message_queue:
                message = message_queue.pop(0)
                yield f"data: {json.dumps(message)}\n\n"

    return Response(event_stream(), content_type='text/event-stream')

def run_server():
    clear_cache_periodically.last_clear = time()
    app.run(host='0.0.0.0', port=5005, threaded=True)

if __name__ == '__main__':
    DatabaseService.init_db()
    run_server()
