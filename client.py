import socket

s = socket.socket()
s.connect(("192.168.0.102", 55555))
print("Connected")
while True:
    data = s.recv(1024)
    if not data:
        break
    print('Received \n', data.decode("utf-8"))