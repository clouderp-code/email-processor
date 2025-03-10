from prometheus_client import Counter, Histogram
import time

# Define metrics
request_counter = Counter('email_processor_requests_total', 'Total requests processed')
processing_time = Histogram('email_processing_duration_seconds', 'Time spent processing emails')
error_counter = Counter('email_processor_errors_total', 'Total processing errors')

def track_request(endpoint: str):
    request_counter.labels(endpoint=endpoint).inc()

def track_processing_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            processing_time.observe(time.time() - start_time)
            return result
        except Exception as e:
            error_counter.inc()
            raise e
    return wrapper 