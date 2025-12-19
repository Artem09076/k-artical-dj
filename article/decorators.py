import time
from functools import wraps

from .metrics import DB_LATENCY


def track_db_latency(method_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed_time = time.time() - start_time
                DB_LATENCY.labels(handler=method_name).observe(elapsed_time)

        return wrapper

    return decorator
