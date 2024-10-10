# utils/helpers.py
import time
from functools import wraps
from config.settings import config
from .logger import Logger
def clean_text(text: str) -> str:
    return ' '.join(text.replace('\t', ' ').replace('\n', ' ').split())

lgr = Logger(config.LOG_TO_FILE, config.LOG_FILE_NAME).get_logger()

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        This is a wrapper for the timeit decorator. It records the start time of a function call, 
        executes the function, records the end time, calculates the difference, and prints the time 
        taken in milliseconds and seconds.
        """
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Execute the function
        end_time = time.time()  # Record the end time
        elapsed_time = (end_time - start_time)  # Calculate time in milliseconds
        elapsed_time_min = elapsed_time / 60

        if elapsed_time < 60:
            lgr.info(f"timeit: --> '{func.__name__}' took {elapsed_time:.4f} seconds to execute")
        else:
            lgr.info(f"timeit: --> '{func.__name__}' took {elapsed_time_min:.2f} minutes to execute")
        return result
    return wrapper
