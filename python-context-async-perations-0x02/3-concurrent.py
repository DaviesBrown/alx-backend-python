import asyncio
import aiosqlite

async def setup_sample_database(db_path):
    """Create a sample SQLite database with users table for demonstration."""
    async with aiosqlite.connect(db_path) as db:
        # Create users table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER
            )
        ''')
        
        # Insert sample data
        sample_users = [
            ('Alice Johnson', 'alice@email.com', 28),
            ('Bob Smith', 'bob@email.com', 35),
            ('Charlie Brown', 'charlie@email.com', 22),
            ('Diana Davis', 'diana@email.com', 41),
            ('Eve Wilson', 'eve@email.com', 19),
            ('Frank Miller', 'frank@email.com', 55),
            ('Grace Lee', 'grace@email.com', 33),
            ('Henry Ford', 'henry@email.com', 67),
            ('Ivy Chen', 'ivy@email.com', 45),
            ('Jack Wilson', 'jack@email.com', 23),
            ('Kate Brown', 'kate@email.com', 52),
            ('Leo Martinez', 'leo@email.com', 38),
            ('Maya Patel', 'maya@email.com', 29),
            ('Noah Davis', 'noah@email.com', 61),
            ('Olivia White', 'olivia@email.com', 26)
        ]
        
        await db.executemany('''
            INSERT OR IGNORE INTO users (name, email, age) 
            VALUES (?, ?, ?)
        ''', sample_users)
        
        await db.commit()
        print("Sample SQLite database setup complete")

async def async_fetch_users(db_path):
    """
    Asynchronous function to fetch all users.
    
    Args:
        db_path (str): Path to the SQLite database
        
    Returns:
        list: All users
    """
    db = await aiosqlite.connect(db_path)
    cursor = await db.execute('SELECT * FROM users ORDER BY name ASC')
    results = await cursor.fetchall()
    await cursor.close()
    await db.close()
    return results

async def async_fetch_older_users(db_path, age):
    """
    Asynchronous function to fetch users older than a specified age.
    
    Args:
        db_path (str): Path to the SQLite database
        age (int): Minimum age for filtering users
        
    Returns:
        list: Users older than the specified age
    """
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute(f"SELECT * FROM users WHERE age > ? ORDER BY age DESC", (age,))
        results = await cursor.fetchall()
        await cursor.close()
        return results

async def fetch_concurrently():
    """
    Function to run multiple database queries concurrently using asyncio.gather().
    """
    db_path = "async.db"
    await setup_sample_database(db_path)

    all_users, older_users = await asyncio.gather(
        async_fetch_users(db_path),
        async_fetch_older_users(db_path, 25)
    )
    # Display results
    print("\n" + "="*60)
    print("QUERY RESULTS")
    print("="*60)
    
    print("\n📊 ALL USERS:")
    print("-" * 50)
    print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Age':<5}")
    print("-" * 50)
    for user in all_users:
        print(f"{user[0]:<5} {user[1]:<20} {user[2]:<25} {user[3]:<5}")
    
    print(f"\n📊 USERS OLDER THAN 40:")
    print("-" * 50)
    print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Age':<5}")
    print("-" * 50)
    for user in older_users:
        print(f"{user[0]:<5} {user[1]:<20} {user[2]:<25} {user[3]:<5}")

def main():
    """
    Main function to demonstrate concurrent database queries.
    """
    asyncio.run(fetch_concurrently())

if __name__ == "__main__":
    main()
