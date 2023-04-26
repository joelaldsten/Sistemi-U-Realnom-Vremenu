import socket

s = socket.create_server(("127.0.0.69", 80))
s.listen()
conn, addr = s.accept()
while True:
    data = conn.recv(1024)
    conn.sendall(b"hello my friend")
    break
