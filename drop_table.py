import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# drop table
cursor.execute("DROP TABLE IF EXISTS soilcore_newsletter;")
conn.commit()
conn.close()

print("✅ Table 'soilcore_newsletter' removed successfully!")
