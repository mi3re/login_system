import socket
import rsa

# rsa keys
public_key, private_key = rsa.newkeys(1024)
public_key_server = None

# connect with the server
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(('localhost', 9999))

# exchange rsa keys with server
public_key_server = rsa.PublicKey.load_pkcs1(c.recv(1024))
c.send(public_key.save_pkcs1("PEM"))

# send username
message = rsa.decrypt(c.recv(1024), private_key).decode()
c.send(rsa.encrypt(input(message).encode(), public_key_server))
# send password
message = rsa.decrypt(c.recv(1024), private_key).decode()
c.send(rsa.encrypt(input(message).encode(), public_key_server))
# print if auth is successful or not
print(rsa.decrypt(c.recv(1024), private_key).decode())