import sqlite3
text = "SELECT * FROM users WHERE username = 'Test'"
conn = sqlite3.connect('grades.db')
cursor = conn.cursor()
cursor.execute(text)
rows = cursor.fetchall()
print(rows)