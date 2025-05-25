import sqlite3
import functools

def log_queries(fn):
    """Decorator that log all queries before sql execution"""
    @functools.wraps(fn)
    def wrapper(query):
        print(query)
        fn(query)
    return wrapper

@log_queries
def fetch_all_users(query):
    """Fetch all users from user table"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")