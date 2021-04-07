import socket
host = '127.0.0.1'
port = 12345
port1 = 12346
port2 = 12347
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
    s1.bind((host, port))
    s1.listen()
    c1, addr1 = s1.accept()
    with c1:
        data1 = c1.recv(2000)
        c1.sendall(b'acknowledged')
        print('received data', data1)
    s1.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
    s2.bind((host, port1))
    s2.listen()
    c2, addr2 = s2.accept()
    with c2:
        data2 = c2.recv(2000)
        c2.sendall(b'acknowledged')
        print('received data', data2)
    s2.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s3:
    s3.bind((host, port2))
    s3.listen()
    c3, addr3 = s3.accept()
    with c3:
        data3 = c3.recv(2000)
        c3.sendall(b'acknowledged')
        print('received data', data3)
    s3.close()