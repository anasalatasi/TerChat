import requests
import uuid
import time
from requests.exceptions import ConnectionError

server_url = "http://localhost:5005"
client_id = str(uuid.uuid4())


def send_message_to_server(text):
    try:
        start_time = time.time()
        response = requests.post(
            f"{server_url}/messages", json={"text": text, "sender": client_id}
        )
        elapsed_time = time.time() - start_time
        print(f"Time taken to send message: {elapsed_time} seconds")
        return (
            "Message sent successfully."
            if response.status_code == 200
            else "Failed to send message."
        )
    except ConnectionError:
        return "Connection to the server failed."


def get_messages_from_server():
    try:
        response = requests.get(f"{server_url}/messages")
        return response.json() if response.status_code == 200 else []
    except ConnectionError:
        return []


def get_message_count_from_server():
    try:
        start_time = time.time()
        response = requests.get(f"{server_url}/messages/count")
        elapsed_time = time.time() - start_time
        print(f"Time taken to get message count: {elapsed_time} seconds")
        return response.json().get("count") if response.status_code == 200 else None
    except ConnectionError:
        return None
