import time
import logging

def retry(max_attempts: int = 3, delay: int = 1, backoff_factor: float = 2):
    """
    Decorator to retry a function with exponential backoff.

    Args:
        max_attempts (int): Maximum number of attempts to make.
        delay (int): Initial delay between attempts in seconds.
        backoff_factor (float): Factor to increase the delay by after each attempt.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            last_exception = None
            delay_seconds = delay

            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    last_exception = e
                    logging.warning(f"Attempt {attempts} failed: {str(e)}")
                    time.sleep(delay_seconds)
                    delay_seconds *= backoff_factor

            logging.error(f"All {max_attempts} attempts failed: {str(last_exception)}")
            raise last_exception

        return wrapper

    return decorator