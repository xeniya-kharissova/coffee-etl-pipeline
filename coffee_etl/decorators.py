from functools import wraps
import time
import logging

logger = logging.getLogger(__name__)


def measure_time(func):
    @wraps(func)   
    def wrapper(*args,**kwargs):
        start = time.perf_counter()
        try:
            result = func(*args,**kwargs)
            return result
        finally:
            elapsed = time.perf_counter() - start
            logger.info(f"[TIME] {func.__name__} выполнилась за {elapsed:.4f} сек.")
        
    return wrapper

def retry(retries : int = 3, delay : float = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    logger.warning(f"[UNEXPECTED ERROR] | [ATTEMPT] : {attempt+1} | [REASON] : {e}")
                    if attempt+1 == retries :
                        logger.error(f"Function {func.__name__} failed after all attempts")
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator
    