from Cryptodome.Cipher import ChaCha20_Poly1305
from numba import jit
import socket
import time

start_time = time.time()

def sockreceive():
    host = '127.0.0.1'
    port = 12345
    port1 = 12346
    port2 = 12347
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
        s1.bind((host, port))
        s1.listen()
        c1= s1.accept()
        with c1:
            data1 = c1.recv(2000)
            c1.sendall(b'acknowledged')
            print('received data', data1)
        s1.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        s2.bind((host, port1))
        s2.listen()
        c2= s2.accept()
        with c2:
            data2 = c2.recv(2000)
            c2.sendall(b'acknowledged')
            print('received data', data2)
        s2.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s3:
        s3.bind((host, port2))
        s3.listen()
        c3= s3.accept()
        with c3:
            data3 = c3.recv(2000)
            c3.sendall(b'acknowledged')
            print('received data', data3)
        s3.close()
    return data1, data2, data3
 
def dec(data1, data2, data3):
    key = b'\x1a\xe0J\xb7\xfe\x18\x08>+\xd9\xb4\xb8,+n#\xef\xc1\x0b\xa2\xa3\x01\x8c\xf4\xd7\x17\xbf\xc9\xc0\x0c\xb0z'
    cipher = ChaCha20_Poly1305.new(key=key, nonce=data3)
    plaintext_b = cipher.decrypt(data1)
    cipher.verify(data2)
    plaintext = int.from_bytes(plaintext_b, byteorder="little",signed=0)
    print(plaintext)

def calc(plaintext):
    plaintext = plaintext ** (1/3)
    angle = plaintext*10
    print("Angle of Servo: ",angle)
    angle_b = angle.to_bytes(length=2, byteorder="little", signed=0)

def enc(angle):
    key = b'\x1a\xe0J\xb7\xfe\x18\x08>+\xd9\xb4\xb8,+n#\xef\xc1\x0b\xa2\xa3\x01\x8c\xf4\xd7\x17\xbf\xc9\xc0\x0c\xb0z'
    cipher = ChaCha20_Poly1305.new(key=key)
    ciphertext_r, tag_r = cipher.encrypt_and_digest(angle_b)
    nnc_r = cipher.nonce
    return ciphertext_r, tag_r, nnc_r

def socksend(ciphertext_r, tag_r, nnc_r):
    host = '127.0.0.1'
    port = 12345
    port1 = 12346
    port2 = 12347
    print(ciphertext_r)
    print(tag_r)
    print(nnc_r)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
        s1.connect((host,port))
        print('sending ciphertext...')
        s1.sendall(ciphertext_r)
        data1 = s1.recv(1024)
        print(data1)
    s1.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        s2.connect((host,port1))
        print('sending tag...')
        s2.sendall(tag_r)
        data2 = s2.recv(1024)
        print(data2)
    s2.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s3:
        s3.connect((host,port2))
        print('sending nnc...')
        s3.sendall(nnc_r)
        data3 = s3.recv(1024)
        print(data3)
    s3.close()

def main():
    data1, data2, data3 = sockreceive()
    dec(data1, data2, data3)
    calc(plaintext)
    ciphertext_r, tag_r, nnc_r = enc(angle_b)
    socksend(ciphertext_r, tag_r, nnc_r)

if __name__ == "__main__":
    main()

Total_time = (time.time()- start_time)
print(Total_time)
