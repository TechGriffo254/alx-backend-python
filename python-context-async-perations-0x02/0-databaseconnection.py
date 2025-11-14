import sqlite3


class DatabaseConnection:
    """Class-based context manager for database connections"""
    
    def __init__(self, db_name):
        """Initialize with database name"""
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        """Open database connection when entering context"""
        self.connection = sqlite3.connect(self.db_name)
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection when exiting context"""
        if self.connection:
            self.connection.close()
        return False


# Use the context manager to query the database
if __name__ == "__main__":
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
