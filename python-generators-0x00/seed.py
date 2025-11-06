#!/usr/bin/python3

"""
seed.py - Sets up the ALX_prodev database  (SQLite3) and seeds it with user data.
"""

import mysql.connector
from mysql.connector import Error
import csv
import os

"""
connect_db() - connects the user to mysql server
"""
def connect_db():
    try:
        connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='my_password'
                )

        if connection.is_connected():
            print("Successfully connected to MySQL server")
            return connection

    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None

"""
create_database(connection) - creates the database, ALX_prodev.
"""
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database AlX_prodev created successfully or already exists")

    except Error as e:
        print(f"Error while creating database: {e}")

    finally:
        cursor.close()


"""
connect_to_prodev() - connects to the created database ALX_prodev
"""
def connect_to_prodev():
    try:
        database_connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='my_password',
                database='ALX_prodev'
                )

        if database_connection.is_connected():
            print("Connected to MySQL database 'ALX_prodev'")
            return database_connection

    except Error as e:
        print(f"Error connecting to MySQL database ALX_prodev: {e}")
        return None


"""
create_table(connection) - creates Table,  user_data, in the database ALX_prodev
"""
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id UUID PRIMARY KEY INDEXED,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        )
        """
        )
        connection.commit()
        print("Table 'user_data' successfully created")

    except Error as e:
        print(f"Error creating table 'user_data': {e}")

    finally
        cursor.close()

"""
insert_data(connection, data) - inserts data in the database if it does not exist
"""
def insert_data(connection, data):
    try:
        cursor = connection.cursor()

        with open(data, mode='r') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                cursor.execute("""
                    INSERT IGNORE INTO users (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (row['user_id'], row['name'], row['email'], row['age']))
          
        connection.commit()
        print("Table 'user_data' successfully updated with CSV data")

    except Error as e:
        print(f"Error updating 'user_data': {e}")

    finally:
        cursor.close()


