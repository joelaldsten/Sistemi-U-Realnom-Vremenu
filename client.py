import socket

s = socket.socket()
s.connect(("kanelbulle.duckdns.org", 55555))
while True:
    data = s.recv(4096)
    print('Received ', repr(data))