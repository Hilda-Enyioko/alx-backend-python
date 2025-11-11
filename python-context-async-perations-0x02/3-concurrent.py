# Objective: Run multiple database queries concurrently using asyncio.gather.
# Instructions:
# Use the aiosqlite library to interact with SQLite asynchronously. To learn more about it, click here.
# Write two asynchronous functions: async_fetch_users() and async_fetch_older_users() that fetches all users and users older than 40 respectively.
# Use the asyncio.gather() to execute both queries concurrently.
# Use asyncio.run(fetch_concurrently()) to run the concurrent fetch

import aiosqlite
import asyncio
#!/usr/bin/python

async def async_fetch_users():
    async with aiosqlite.connect('users.db') as conn:
        cursor = await conn.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        await cursor.close()
        return users
    
async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as conn:
        cursor = await conn.execute("SELECT * FROM users WHERE age > ?", (40,))
        older_users = await cursor.fetchall()
        await cursor.close()
        return older_users

async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:", users)
    print("Users older than 40:", older_users)
    
#### Run the concurrent fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())()