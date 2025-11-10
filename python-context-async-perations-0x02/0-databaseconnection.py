# Objective: create a class based context manager to handle opening and closing database connections automatically
# Instructions:
#   Write a class custom context manager DatabaseConnection using the __enter__ and the __exit__ methods
#   Use the context manager with the with statement to be able to perform the query SELECT * FROM users. Print the results from the query.

import sqlite3

#!/usr/bin/python
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

#### Using the DatabaseConnection context manager to fetch users
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print(users)