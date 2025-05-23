import time
import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator that handles database connections automatically.

    Args:
        func: The function to be decorated

    Returns:
        A wrapper function that manages database connections
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open connection to the database
        conn = sqlite3.connect("users.db")

        try:
            # Pass the connection as the first argument to the function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Close the connection regardless of success or failure
            conn.close()

    return wrapper


def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries a function if it raises an exception.

    Args:
        retries: Maximum number of retries (default: 3)
        delay: Time to wait between retries in seconds (default: 2)

    Returns:
        A decorator function that implements retry logic
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Track the number of attempts
            attempts = 0

            # Try up to 'retries' times
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    # If this was the last attempt, re-raise the exception
                    if attempts == retries:
                        raise e

                    # Otherwise, wait and retry
                    print(
                        f"Operation failed. Retrying in {delay} seconds... (Attempt {attempts}/{retries})"
                    )
                    time.sleep(delay)

        return wrapper

    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Example usage:
if __name__ == "__main__":
    # Attempt to fetch users with automatic retry on failure
    users = fetch_users_with_retry()
    print(users)
