import socket

port = 5050

sock = socket.socket()
sock.bind(('', port))
sock.listen()
client = []  # Массив где храним адреса клиентов
print('Start Server on port = ', port)

while 1:
    conn, adr = sock.accept()
    print(conn, adr)
    conn.send("asd".encode())

    data = conn.recv(1024)
    print(data.decode("utf-8"))


