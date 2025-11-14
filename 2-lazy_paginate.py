#!/usr/bin/env python3
"""
Module for lazy loading paginated data using generators.
"""
import seed


def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database.
    
    Args:
        page_size (int): Number of users per page
        offset (int): Starting position for fetching data
        
    Returns:
        list: A list of user records as dictionaries
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily loads paginated data.
    Only fetches the next page when needed.
    
    Args:
        page_size (int): Number of records per page
        
    Yields:
        list: A page of user records
    """
    offset = 0
    
    while True:
        page = paginate_users(page_size, offset)
        
        # Stop if no more data
        if not page:
            break
            
        yield page
        offset += page_size
