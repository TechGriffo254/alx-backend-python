#!/usr/bin/env python3
"""
Module for memory-efficient age aggregation using generators.
"""
import mysql.connector


def stream_user_ages():
    """
    Generator that yields user ages one by one.
    Memory-efficient approach to processing large datasets.
    
    Yields:
        int: User age
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Update with your MySQL password
            database='ALX_prodev'
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        # Yield ages one by one
        for (age,) in cursor:
            yield age
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as e:
        print(f"Database error: {e}")


def calculate_average_age():
    """
    Calculates the average age of users without loading
    the entire dataset into memory.
    Uses the stream_user_ages generator for memory efficiency.
    """
    total_age = 0
    count = 0
    
    # Process ages one at a time using generator
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found in database")


# Execute when run directly
if __name__ == "__main__":
    calculate_average_age()
