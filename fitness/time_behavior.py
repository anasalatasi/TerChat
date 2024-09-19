import requests
import time
import concurrent.futures
import socketio
import statistics

BASE_URL = "http://localhost:5005"

def send_message(text, sender):
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/messages", json={"text": text, "sender": sender})
    end_time = time.time()
    return response.status_code == 200, end_time - start_time

def get_messages():
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/messages")
    end_time = time.time()
    return response.status_code == 200, end_time - start_time

def get_message_count():
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/messages/count")
    end_time = time.time()
    return response.status_code == 200, end_time - start_time

def test_socket_connection():
    sio = socketio.Client()
    try:
        start_time = time.time()
        sio.connect(BASE_URL)
        time.sleep(1)
        sio.disconnect()
        end_time = time.time()
        return True, end_time - start_time
    except Exception as e:
        print(f"Socket connection error: {e}")
        return False, 0

def run_load_test(num_requests, num_threads):
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        print("Submitting requests...")
        for i in range(num_requests):
            futures.append(executor.submit(send_message, f"Test message {i}", f"Sender {i}"))
            futures.append(executor.submit(get_messages))
            futures.append(executor.submit(get_message_count))
        
            if i % 10 == 0:
                futures.append(executor.submit(test_socket_connection))

        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    end_time = time.time()
    success_rate = sum(result[0] for result in results) / len(results) * 100
    total_time = end_time - start_time
    requests_per_second = num_requests / total_time

    response_times = [result[1] for result in results]
    max_response_time = max(response_times)
    avg_response_time = statistics.mean(response_times)
    std_dev_response_time = statistics.stdev(response_times)

    print(f"Load Test Results:")
    print(f"Total Requests: {num_requests}")
    print(f"Number of Threads: {num_threads}")
    print(f"Success Rate: {success_rate:.2f}%")
    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Requests per Second: {requests_per_second:.2f}")
    print(f"Max Response Time: {max_response_time:.4f} seconds")
    print(f"Average Response Time: {avg_response_time:.4f} seconds")
    print(f"Standard Deviation of Response Time: {std_dev_response_time:.4f} seconds")

if __name__ == "__main__":
    run_load_test(num_requests=10000, num_threads=10)