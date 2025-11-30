import aiosqlite
import asyncio


async def async_fetch_users():
    """Fetch all users from the database asynchronously"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All users:")
            for row in results:
                print(row)
            return results


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in results:
                print(row)
            return results


async def fetch_concurrently():
    """Execute both queries concurrently using asyncio.gather"""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results


# Run the concurrent fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
