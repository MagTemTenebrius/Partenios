import socket
import threading

sock = socket.socket()
sock.connect(("localhost", 5050))


def read(sock):
    data = sock.recv(1024)
    print("Server: " + data.decode("utf-8"))
    pass


def write(sock):
    while (1):
        msg = input()
        sock.send(msg.encode())


read_thread = threading.Thread(target=read, args=(sock,))
read_thread.start()
write_thread = threading.Thread(target=write, args=(sock,))
write_thread.start()

msg = input()
sock.send(msg.encode())

# sock.send("Hello, server".encode())
