import time
import sqlite3
import functools

# Dictionary to store query results
query_cache = {}


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
        conn = sqlite3.connect('users.db')
        
        try:
            # Pass the connection as the first argument to the function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Close the connection regardless of success or failure
            conn.close()
    
    return wrapper


def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string.
    
    Args:
        func: The function to be decorated
        
    Returns:
        A wrapper function that implements query caching
    """
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Check if the query result is already in the cache
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]
        
        # If not in cache, execute the function
        result = func(conn, query, *args, **kwargs)
        
        # Store the result in the cache
        query_cache[query] = result
        print(f"Cached result for query: {query}")
        
        return result
    
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Example usage:
if __name__ == "__main__":
    # First call will cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"First call result: {len(users)} users")
    
    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Second call result: {len(users_again)