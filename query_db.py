import sqlite3

conn = sqlite3.connect('instance/test.db')
cursor = conn.execute("SELECT *  FROM User")
# cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
rows = cursor.fetchall()
print(rows)