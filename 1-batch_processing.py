#!/usr/bin/env python3
"""
Module for batch processing large datasets using generators.
"""
import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows in batches from the user_data table.
    
    Args:
        batch_size (int): Number of rows to fetch per batch
        
    Yields:
        list: A batch of user records as dictionaries
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Update with your MySQL password
            database='ALX_prodev'
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as e:
        print(f"Database error: {e}")


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.
    
    Args:
        batch_size (int): Number of rows to process per batch
    """
    # Process batches
    for batch in stream_users_in_batches(batch_size):
        # Filter users over age 25
        for user in batch:
            if user['age'] > 25:
                print(user)
