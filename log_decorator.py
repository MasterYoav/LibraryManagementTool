import os
import functools
from datetime import datetime

# Log file path
LOG_FILE = "log.txt"

# Ensure the log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as file:
        file.write("--- Library Log ---\n")

def log_decorator(action):
    """
    Decorator to log actions to a file.

    Parameters:
        action (str): The action being performed, to include in the log message.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                log_message = f"[{datetime.now()}] {action} completed successfully.\n"
                with open(LOG_FILE, "a") as log_file:
                    log_file.write(log_message)
                return result
            except Exception as e:
                log_message = f"[{datetime.now()}] {action} failed: {str(e)}\n"
                with open(LOG_FILE, "a") as log_file:
                    log_file.write(log_message)
                raise e
        return wrapper
    return decorator

# Example usage
if __name__ == "__main__":
    @log_decorator("Add book")
    def add_book_example():
        # Simulating adding a book
        print("Book added!")

    @log_decorator("Remove book")
    def remove_book_example():
        # Simulating removing a book
        print("Book removed!")

    try:
        add_book_example()
        remove_book_example()
    except Exception as error:
        print(f"An error occurred: {error}")
