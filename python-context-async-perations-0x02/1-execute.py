import mysql.connector
from mysql.connector import Error

class ExecuteQuery:
    """
    A context manager that takes a query as input and executes it, 
    managing both connection and the query execution
    """
    
    def __init__(
            self,
            query,
            params,
            host='localhost',
            database=None,
            user=None,
            password=None,
            port=3306
        ):
        """
        Initialize the ExecuteQuery context manager.
        
        Args:
            query (str): SQL statement to execute
            params (tuple): Params for the query
            host (str): MySQL server host (default: localhost)
            database (str): Database name
            user (str): MySQL username
            password (str): MySQL password
            port (int): MySQL server port (default: 3306)
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None
        self.cursor = None
        self.query = query
        self.params = params or ()
        self.result = None
    
    def __enter__(self):
        """
        Enter the context manager - establish MySQL database connection and execute query.
        
        Returns:
            list: Query result
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                autocommit=False
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                if self.params:
                    self.cursor.execute(self.query, self.params)
                else:
                    self.cursor.execute(self.query)
                self.result = self.cursor.fetchall()
                return self.result
            else:
                raise Error("Failed to establish connection")
                
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager - close MySQL database connection.
        
        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
        """
        if self.cursor:
            self.cursor.close()
        
        if self.connection and self.connection.is_connected():
            if exc_type is None:
                self.connection.commit()
                print("MySQL database changes committed successfully")
            else:
                self.connection.rollback()
                print(f"Exception occurred, rolling back changes: {exc_val}")
            self.connection.close()
            print("MySQL database connection closed")
        return False

def main():
    """Demonstrate the MySQL ExecuteQuery context manager."""
    query = "SELECT * FROM users WHERE age > %s"
    params = (25,)

    connection_params = {
        'host': 'localhost',
        'database': 'test_db',
        'user': 'root',
        'password': 'password',
        'port': 3306
    }
    
    print("MySQL Execute Query Context Manager Demo")
    print("="*50)
    
    try:
        with ExecuteQuery(query, params, **connection_params) as results:
            print("\nQuery Results:")
            print("-" * 50)
            print(f"{'ID':<5} {'Name':<15} {'Email':<25} {'Age':<5}")
            print("-" * 50)
            for row in results:
                print(f"{row[0]:<5} {row[1]:<15} {row[2]:<25} {row[3]:<5}")
            print(f"\nTotal users found: {len(results)}") 
    except Error as e:
        print(f"MySQL Error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
