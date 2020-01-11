import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

users_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(users_table)

item_table = "CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(item_table)

# cursor.execute("INSERT INTO item VALUES('test', 10.90)")

connection.commit()
connection.close()
