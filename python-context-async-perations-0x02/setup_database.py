import sqlite3

# Create database and users table
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    age INTEGER
)
''')

# Insert sample data with various ages
sample_users = [
    ('Alice Johnson', 'alice.johnson@example.com', 28),
    ('Bob Smith', 'bob.smith@example.com', 35),
    ('Charlie Brown', 'charlie.brown@example.com', 42),
    ('Diana Prince', 'diana.prince@example.com', 31),
    ('Eve Williams', 'eve.williams@example.com', 26),
    ('Frank Miller', 'frank.miller@example.com', 45),
    ('Grace Lee', 'grace.lee@example.com', 38),
    ('Henry Davis', 'henry.davis@example.com', 52),
    ('Iris Chen', 'iris.chen@example.com', 29),
    ('Jack Wilson', 'jack.wilson@example.com', 41)
]

cursor.executemany('INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)', sample_users)

conn.commit()
conn.close()

print("Database setup complete! Created 'users.db' with sample data.")
print("Users include ages ranging from 26 to 52 for testing queries.")
