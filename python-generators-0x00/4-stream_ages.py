#!/usr/bin/python3
"""
Module for memory-efficient aggregation of user ages using generators.
"""
from seed import connect_to_prodev


def stream_user_ages():
    """
    Generator that yields user ages one by one.

    Yields:
        User age as a float
    """
    connection = connect_to_prodev()
    cursor = connection.cursor()

    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield float(age)

    cursor.close()
    connection.close()


def average_user_age():
    """
    Calculate and print the average age of users without loading the entire dataset.
    Uses the stream_user_ages generator for memory efficiency.
    """
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    if count > 0:
        print(f"Average age of users: {total / count:.2f}")
    else:
        print("No users in database.")
