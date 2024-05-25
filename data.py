import sqlite3
import hashlib

# connect to database
conn = sqlite3.connect('database.db')
cur = conn.cursor()

# create database if it doesn't exist (database contains id, username and password fields)
cur.execute("""CREATE TABLE IF NOT EXISTS database(
id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL)""")

# sample data (username, hashed password)
username1, password1 = "john213", hashlib.sha256("johnlikescats123".encode()).hexdigest()
username2, password2 = "marysmith", hashlib.sha256("marysmith2004".encode()).hexdigest()
username3, password3 = "andrew07", hashlib.sha256("andrewcanary90".encode()).hexdigest()
username4, password4 = "markbinsky", hashlib.sha256("markgaming777".encode()).hexdigest()
username5, password5 = "megan1998", hashlib.sha256("meganjones1998".encode()).hexdigest()

# add sample data to database
cur.execute("INSERT INTO database (username, password) VALUES (?, ?)", (username1, password1))
cur.execute("INSERT INTO database (username, password) VALUES (?, ?)", (username2, password2))
cur.execute("INSERT INTO database (username, password) VALUES (?, ?)", (username3, password3))
cur.execute("INSERT INTO database (username, password) VALUES (?, ?)", (username4, password4))
cur.execute("INSERT INTO database (username, password) VALUES (?, ?)", (username5, password5))

conn.commit()