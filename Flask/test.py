import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('instance/subscribers.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Execute an SQL query
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch and print all rows from the result
tables = cursor.fetchall()
print(tables)

# Close the connection
conn.close()

