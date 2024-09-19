import requests
import time
import concurrent.futures
import socketio

BASE_URL = "http://localhost:5005"

def send_message(text, sender):
    response = requests.post(f"{BASE_URL}/messages", json={"text": text, "sender": sender})
    return response.status_code == 200

def get_messages():
    response = requests.get(f"{BASE_URL}/messages")
    return response.status_code == 200

def get_message_count():
    response = requests.get(f"{BASE_URL}/messages/count")
    return response.status_code == 200

def test_socket_connection():
    sio = socketio.Client()
    try:
        sio.connect(BASE_URL)
        time.sleep(1)
        sio.disconnect()
        return True
    except Exception as e:
        print(f"Socket connection error: {e}")
        return False

def run_load_test(num_requests, num_threads):
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(num_requests):
            futures.append(executor.submit(send_message, f"Test message {i}", f"Sender {i}"))
            futures.append(executor.submit(get_messages))
            futures.append(executor.submit(get_message_count))
        
        if i % 10 == 0:
            futures.append(executor.submit(test_socket_connection))

        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    end_time = time.time()
    success_rate = sum(results) / len(results) * 100
    total_time = end_time - start_time
    requests_per_second = num_requests / total_time

    print(f"Load Test Results:")
    print(f"Total Requests: {num_requests}")
    print(f"Number of Threads: {num_threads}")
    print(f"Success Rate: {success_rate:.2f}%")
    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Requests per Second: {requests_per_second:.2f}")

if __name__ == "__main__":
    run_load_test(num_requests=10000, num_threads=10)