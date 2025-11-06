"""
2-lazy_paginate.py - fetches paginated data from the users database using a generator to lazily load each page
"""

import mysql.connector
from mysql.connector import Error

"""
paginate_users(page_size, offset) - only fetches  only fetch the next page when needed at an offset of 0.
"""
#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


"""
lazy_paginate(page_size) - yields pages of data lazily
"""
def lazy_paginate(page_size):
    
    offset = 0

    while True:
        page = paginate_users(page_size, offset)

        if not page:
            break

        yield page
        offset += page_size
