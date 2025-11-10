# Objective: create a decorator that logs database queries executed by any function

#!/usr/bin/python
import sqlite3
import functools

#### decorator to lof SQL queries

""" YOUR CODE GOES HERE"""
def log_queries(func):
    @functools.wraps(func)
    def wrapper_log_queries(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            print(f"Executing SQL query: {query}")
        else:
            print("No SQL query provided.")
        return func(*args, **kwargs)
    return wrapper_log_queries

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")