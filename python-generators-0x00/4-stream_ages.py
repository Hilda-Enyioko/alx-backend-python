"""
 4-stream_ages.py -
 a generator to compute a memory-efficient aggregate function
 i.e. that is average age for a large dataset
"""

import mysql.connector
from mysql.connector import Error

"""
stream_user_ages() - yields user ages one by one
"""


def stream_user_ages():
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='my_password',
            database='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT age FROM user_data")

        for row in cursor:
            if not row:
                break

            yield row

    except Error as e:
        print(f"Database error: {e}")

    finally:
        cursor.close()


def compute_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found")
        return

    average_age = total_age / count

    print(f"Average age of users: {average_age}")


if __name__ == "__main__":
    compute_average_age()
