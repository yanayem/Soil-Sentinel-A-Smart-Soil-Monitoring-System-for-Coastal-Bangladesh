import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print table names in a cleaner format
print("Tables in db.sqlite3:")
for table in tables:
    print("-", table[0])

# Close connection
conn.close()
