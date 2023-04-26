import socket

s = socket.create_server(("GUI", 42069))
s.listen()
conn, addr = s.accept()
while True:
    data = conn.recv(1024)
