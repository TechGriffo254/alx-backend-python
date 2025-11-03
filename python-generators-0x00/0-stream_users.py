#!/usr/bin/env python3
"""
Module for streaming users from the database using generators.
"""
import mysql.connector


def stream_users():
    """
    Generator that streams rows from the user_data table one by one.
    Uses yield to provide memory-efficient iteration over database rows.
    
    Yields:
        dict: A dictionary containing user data (user_id, name, email, age)
    """
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Update with your MySQL password
            database='ALX_prodev'
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        # Yield rows one by one
        for row in cursor:
            yield row
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
