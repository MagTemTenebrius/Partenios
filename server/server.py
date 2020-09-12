import socket

port = 5050

sock = socket.socket()
sock.bind(('', port))
sock.listen()
users = []  # Массив где храним адреса клиентов
print('[Partenios][Server] Server is running on the port ', port)

while 1:
    conn, adr = sock.accept()
    print(conn, '\n', adr)
    conn.send("Hello, user".encode())

    data = conn.recv(1024)
    print(data.decode("utf-8"))


