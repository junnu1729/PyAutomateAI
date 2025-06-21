from prometheus_client import start_http_server, Summary
import time
import random
REQUEST_TIME = Summary("request_processing_seconds", "Time spent processing request")
@REQUEST_TIME.time()
def process_task():
    print("Task executed")
    time.sleep(random.uniform(0.1, 1.0))
if __name__ == "__main__":
    start_http_server(8001)
    print("Prometheus monitoring started at http://localhost:8001/metrics")
    while True:
        process_task()
        time.sleep(5)