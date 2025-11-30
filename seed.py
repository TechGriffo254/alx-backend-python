#!/usr/bin/env python3
"""
Database seeding module for ALX_prodev database.
This module handles database creation, table creation, and data insertion.
"""
import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    """
    Connects to the MySQL database server.
    
    Returns:
        connection object if successful, None otherwise
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # Update with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    
    Returns:
        connection object if successful, None otherwise
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Update with your MySQL password
            database='ALX_prodev'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.
    
    Args:
        connection: MySQL connection object to ALX_prodev database
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3, 0) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """
    Inserts data into the database if it does not exist.
    
    Args:
        connection: MySQL connection object to ALX_prodev database
        csv_file: path to the CSV file containing user data
    """
    try:
        cursor = connection.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"Data already exists ({count} rows). Skipping insertion.")
            cursor.close()
            return
        
        # Read and insert data from CSV
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            insert_query = """
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """
            
            for row in csv_reader:
                # Generate UUID if not present or use existing
                user_id = row.get('user_id', str(uuid.uuid4()))
                name = row.get('name', '')
                email = row.get('email', '')
                age = int(row.get('age', 0))
                
                cursor.execute(insert_query, (user_id, name, email, age))
            
            connection.commit()
            print(f"Data inserted successfully from {csv_file}")
        
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file '{csv_file}' not found")
    except Exception as e:
        print(f"Unexpected error: {e}")
