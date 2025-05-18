#!/usr/bin/python3
"""
Generator function to stream rows from the user_data table in the ALX_prodev database.
"""
from seed import connect_to_prodev


def stream_users():
    """
    Generator function that yields rows from the user_data table one by one.
    Each row is returned as a dictionary with user_id, name, email, and age keys.

    Returns:
        Generator yielding dictionaries with user data
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()
    connection.close()
