import sqlite3 
import functools


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect('users.db')
        result = func(connection, *args, **kwargs)
        connection.close()
        return result
    return wrapper

"""your code goes here"""
def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = kwargs.get('connection')
        if connection is None:
            raise ValueError("No DB connection found")
        try:
            result = func(*args, **kwargs)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()
        return result
    return wrapper


@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
    
#### Update user's email with automatic transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')