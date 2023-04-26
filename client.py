import socket

s = socket.socket()
s.connect(("kanelbulle.duckdns.org", 55555))
s.sendall(b'Hello, world')
data = s.recv(1024)
print('Received', repr(data))