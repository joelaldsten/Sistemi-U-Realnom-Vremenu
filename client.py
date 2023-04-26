import socket

s = socket.socket()
s.connect(("127.0.0.69", 80))
s.sendall(b'Hello, world')
data = s.recv(1024)
print('Received', repr(data))