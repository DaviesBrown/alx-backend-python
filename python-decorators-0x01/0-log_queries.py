import sqlite3
import functools

def log_queries(fn):
    """Log all queries before sql execution"""
    def wrapper(query):
        print(query)
        fn(query)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query=f"INSERT INTO users (id, name, age, email) VALUES ({num}, {row['name']}, {row['age']}, {row['email']})")
