import requests

server_url = 'http://localhost:5000'

def send_message_to_server(text):
    response = requests.post(f'{server_url}/messages', json={'text': text})
    return 'Message sent successfully.' if response.status_code == 200 else 'Failed to send message.'

def get_messages_from_server():
    response = requests.get(f'{server_url}/messages')
    return response.json() if response.status_code == 200 else []

def get_message_count_from_server():
    response = requests.get(f'{server_url}/messages/count')
    return response.json().get('count') if response.status_code == 200 else None
