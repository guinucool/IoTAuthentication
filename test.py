#import socket

#server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.bind(('127.0.0.1', 9091))
#server.listen()

#conn, addr = server.accept()

#print(conn)
#print(addr)

#print(conn.recv(1))
#print(conn.recv(1))
#print(conn.recv(1))

#xd = b'1'
#xd = b'1'
#print(xd)
#print(len(xd))

#print(b'Hello')

a = 1020

a.to_bytes(4, 'little')

final = bytes()
data = [b'2132', b'1232']

for info in data:

    final += info

print(bytes(data))