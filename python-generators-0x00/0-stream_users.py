#!/usr/bin/python3

"""
0-streams_users.py - Generator that streams user_data rows from SQLite table in a database
"""

import mysql.connector
from mysql.connector import Error

"""
stream_users() - fetches rows from user_data one by one returning them as objects
"""

def stream_users():
    
    connection = None
    cursor = None

    try:
        connection = mysql. connector.connect(
                host='localhost',
                user='root',
                password='my_password',
                database='ALX_prodev'
                )

        # This cursor returns a dicts
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

        except Error as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()
            connection.close()
