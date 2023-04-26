import socket
import subprocess
subprocess.call(['sh', './duck.sh'])
s = socket.create_server(("", 55555))
s.listen()
conn, addr = s.accept()
while True:
    data = conn.recv(1024)
    conn.sendall(b"hello my friend")
    break
