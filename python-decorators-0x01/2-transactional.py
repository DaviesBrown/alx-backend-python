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

def transactional(func):
    """
    Wraps a DB-using function in a transaction: commits if all goes well,
    or rolls back if an exception is raised.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("SQLite database changes committed successfully")
            return result
        except Exception:
            conn.rollback()
            print("Exception occurred, rolling back changes")
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    finally:
        cursor.close()

# Usage:
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
