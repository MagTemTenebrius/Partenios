import socket
import threading
import sys
from time import sleep

sock = socket.socket()
sock.connect(("localhost", 5050))


def read_data(sock):
    while 1:
        msg = sock.recv(10).decode("utf-8")
        if msg == '':
            # print("empty package")
            continue
        # try:
        size = int(msg)
        data = ""
        while size > 0:
            newdata = sock.recv(size if size <= 1024 else 1024).decode("utf-8")
            size -= 1024
            data = data + newdata
        print("Server:", data)
        if data == "disconnect":
            exit()
        # except ValueError:
        #     print("Vrong value")
        #     continue

def send_data(sock, msg):
    size = len(msg)
    sock.send((str(size)).encode())
    print("send size:", str(size))
    while not size == 0:
        print("send", msg[:1024])
        sock.send(msg[:1024].encode())
        msg = msg[1024:]
        size = int(size / 1024)


def get_data(sock):
    size = int(sock.recv(10).decode("utf-8"))
    data = ""
    print("size:", size)
    while size > 0:
        newdata = sock.recv(size if size <= 1024 else 1024).decode("utf-8")
        size -= 1024
        print("read:", newdata)
        data = data + newdata
    print("i'm read: " + data)
    return data

def write(sock):
    while 1:
        msg = input()
        send_data(sock, msg)

threads = []

read_thread = threading.Thread(target=read_data, args=(sock,))
threads.append(read_thread)
threads[0].start()
write_thread = threading.Thread(target=write, args=(sock,))
threads.append(write_thread)
threads[1].start()

# sock.send("Hello, server".encode())
