import time
import sqlite3 
import functools
from sqlite3 import Error


query_cache = {}

def with_db_connection(func):
    """Opens and closes the DB connection around each call, returning func’s result."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('async.db')
            return func(conn, *args, **kwargs)
        except Error as e:
            print(f"Error connecting to SQLite database: {e}")
            raise  # re-raise if you want callers to see it
        finally:
            if conn:
                conn.close()
    return wrapper

def cache_query(func):
    """Cache query results"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        if 'query' in kwargs:
            sql = kwargs['query']
        elif args:
            sql = args[0]
        else:
            raise ValueError("SQL query param is missing")

        if sql in query_cache:
            print(f"Cache hited, using cached result for: {sql}")
            return query_cache[sql]
        print("Cache missed, query not in cache")
        result =  func(conn, *args, **kwargs)
        query_cache[sql] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)