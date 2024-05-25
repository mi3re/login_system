import socket
import threading
import sqlite3
import hashlib
import rsa

# rsa keys
public_key, private_key = rsa.newkeys(1024)
public_key_client = None

# start server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 9999))
s.listen()


# communicate with clients
def handle_client(c):
    # request username
    c.send(rsa.encrypt('Username: '.encode(), public_key_client))
    username = rsa.decrypt(c.recv(1024), private_key).decode()
    # request password
    c.send(rsa.encrypt('Password: '.encode(), public_key_client))
    password = rsa.decrypt(c.recv(1024), private_key)
    # hash password
    password = hashlib.sha256(password).hexdigest()

    # connect to database
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    # compare requested username and password from client with the data in the database
    cur.execute("SELECT * FROM database WHERE username = ? AND password = ?", (username, password))

    # if data from client and database match
    if cur.fetchall():
        # logged in successfully
        c.send(rsa.encrypt('Login successful!'.encode(), public_key_client))
    else:
        # not logged in
        c.send(rsa.encrypt('Login failed!'.encode(), public_key_client))


# accept connection with clients
while True:
    c, addr = s.accept()

    # exchange rsa keys with client
    c.send(public_key.save_pkcs1("PEM"))
    public_key_client = rsa.PublicKey.load_pkcs1(c.recv(1024))

    thread = threading.Thread(target=handle_client, args=(c,)).start()