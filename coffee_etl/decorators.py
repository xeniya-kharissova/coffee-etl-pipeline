from functools import wraps
import time


def measure_time(func):
    @wraps(func)   
    def wrapper(*args,**kwargs):
        start = time.perf_counter()
        try:
            result = func(*args,**kwargs)
            return result
        finally:
            elapsed = time.perf_counter() - start
            print(f"[TIME] {func.__name__} выполнилась за {elapsed:.4f} сек.")
        
    return wrapper

def retry(retries : int = 3, delay : float = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for trial in range(retries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"[UNEXPECTED ERROR] | [TRIAL] : {trial+1} | [REASON] : {e}")
                    if trial+1 == retries : raise
                    time.sleep(delay)
        return wrapper
    return decorator
    