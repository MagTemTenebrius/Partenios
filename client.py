import socket

sock = socket.socket()
sock.connect(("localhost", 5050))
data = sock.recv(1024)
print(data.decode("utf-8"))
# while 1:
#     msg = input()
#     sock.send(msg.encode())
sock.send("Hello, server".encode())