#!/usr/bin/python3
"""
Lazy pagination module to fetch paginated data from the users database.
"""
from seed import connect_to_prodev


def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database.

    Args:
        page_size: Number of records per page
        offset: Starting position for the query

    Returns:
        List of user dictionaries for the requested page
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily loads each page of users when needed.

    Args:
        page_size: Number of records per page

    Yields:
        List of user dictionaries for each page
    """
    offset = 0

    while True:
        page = paginate_users(page_size, offset)

        if not page:
            break

        yield page
        offset += page_size
