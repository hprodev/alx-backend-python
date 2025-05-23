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
        conn = sqlite3.connect('users.db')
        
        try:
            # Pass the connection as the first argument to the function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Close the connection regardless of success or failure
            conn.close()
    
    return wrapper


def transactional(func):
    """
    Decorator that wraps a function in a database transaction.
    If the function succeeds, changes are committed.
    If the function raises an error, changes are rolled back.
    
    Args:
        func: The function to be decorated
        
    Returns:
        A wrapper function that manages transactions
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Execute the function
            result = func(conn, *args, **kwargs)
            # If successful, commit the transaction
            conn.commit()
            return result
        except Exception as e:
            # If an error occurs, roll back the transaction
            conn.rollback()
            # Re-raise the exception to be handled by the caller
            raise e
    
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Example usage:
if __name__ == "__main__":
    # Update user's email with automatic transaction handling
    update_user_email(user_id=1, new_email='Cr