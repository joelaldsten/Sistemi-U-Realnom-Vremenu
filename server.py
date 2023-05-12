import socket
import subprocess
#subprocess.call(['sh', './duck.sh'])
s = socket.create_server(("192.168.0.105", 55555))
print("created server")
s.listen()
print("listen")
conn, addr = s.accept()
print("accepted")
for i in range(10):
    conn.sendall(b"hello!")
