import time
import statistics
import requests

response_times = []

# Simulate sending multiple requests and recording response times
for _ in range(100):  # You can change the sample size
    start_time = time.time()
    response = requests.post(
        f"http://192.168.31.171:5005/messages",
        json={"text": "Test", "sender": 0},
    )
    elapsed_time = time.time() - start_time
    response_times.append(elapsed_time)

# Calculate average, max, and standard deviation
average_time = sum(response_times) / len(response_times)
max_time = max(response_times)
std_deviation = statistics.stdev(response_times)

print(f"Average Response Time: {average_time} seconds")
print(f"Max Response Time: {max_time} seconds")
print(f"Standard Deviation: {std_deviation} seconds")
