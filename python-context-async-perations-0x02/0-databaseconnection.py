import mysql.connector

class DatabaseConnection():
    """
        Context manager class for database connection
    """
    
    def __init__(self):
        self.conn = None
    
    def __enter__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        
        return self.conn
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        if exc_type is not None:
            return False
        return True
    
# Usage

if __name__ == "__main__":
    with DatabaseConnection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            print(row)