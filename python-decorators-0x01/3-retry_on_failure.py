import time
import sqlite3 
import functools
from sqlite3 import Error

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

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries the wrapped function up to `retries` times
    if it raises an exception, waiting `delay` seconds between attempts.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for retry in range(1, retries + 1):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    last_exc = e
                    print(f"Execution of {retry} failed, retrying in {delay} seconds..")
                    time.sleep(delay)
            print(f"All {retries} retries attempt failed")
            raise last_exc
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    return cursor.fetchall()

users = fetch_users_with_retry()
print(users)