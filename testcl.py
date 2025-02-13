import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 9091))

client_socket.sendall(b'123')
client_socket.send()

while True:
    pass