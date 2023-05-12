import socket

s = socket.socket()
s.connect(("192.168.0.103", 55555))
print("Connected")
while True:
    data = s.recv(1024).decode("utf-8")
    if data.startswith("PID"):
        print(data.split(" "))
    elif data.startswith("POS"):
        print('Received x = {}, y = {}\n'.format(data.split("|")[1], data.split("|")[2]))
    else:
        print("Received unknown data")
    if not data:
        break