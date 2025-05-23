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


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Example usage:
if __name__ == "__main__":
    # Fetch user by ID with automatic connection handling
    user = get_user_by_id(user_id=1)
    print(user)
