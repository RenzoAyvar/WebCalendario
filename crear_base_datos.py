import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS eventos_academicos
             (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre text, fecha date, hora time)''')

conn.commit()
conn.close()