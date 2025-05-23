import sqlite3
import functools


def log_queries(func):
    """
    Decorator that logs the SQL query before executing the function.

    Args:
        func: The function to be decorated

    Returns:
        A wrapper function that logs queries
    """

    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        # Log the SQL query before execution
        print(f"Query: {query}")
        # Execute the original function
        return func(query, *args, **kwargs)

    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage:
if __name__ == "__main__":
    # Fetch users while logging the query
    users = fetch_all_users(query="SELECT * FROM users")
