import sqlite3


class ExecuteQuery:
    """Reusable context manager for executing database queries"""
    
    def __init__(self, db_name, query, params=None):
        """
        Initialize with database name, query, and parameters
        
        Args:
            db_name: Name of the database file
            query: SQL query to execute
            params: Parameters for the query (optional)
        """
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """Open connection, execute query, and return results"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close cursor and connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        return False


# Use the context manager to execute a query
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)
    
    with ExecuteQuery('users.db', query, param) as results:
        for row in results:
            print(row)
