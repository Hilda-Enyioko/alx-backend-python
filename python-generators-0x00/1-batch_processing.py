#!/usr/bin/python3

"""
1-batch_processing.py - a generator to fetch and process data in batches from the users database
"""

import mysql.connector
from mysql.connector import Error

"""
stream_users_in_batches(batch_size) - fetches rows in table in batches
"""
def stream_users_in_batches(batch_size):
    connection = None
    cursor = None

    try:
        connector = mysql.connector.connect(
                host='localhost',
                user='root',
                password='my_password',
                database='ALX_prodev'
                )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)

            if not batch:
                break

            yield batch

        print("Rows successfully fetched in batches. Batch ended.")

    except Error as e:
        print(f"Database error: {e}")

    finally:
        cursor.close()
        connection.close()


"""
 batch_processing(batch_size) - processes each batch to filter users over the age of 25
"""
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered_batch = []

        for row in batch:
            if row['age'] > 25:
                filtered_batch.append(row)

        return filtered_batch

