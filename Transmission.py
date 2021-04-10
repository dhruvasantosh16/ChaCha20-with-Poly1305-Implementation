from Cryptodome.Cipher import ChaCha20_Poly1305
from Cryptodome.Random import get_random_bytes
from Cryptodome.Random.random import randint  
import time
import socket

#Timing Start
time_start = time.time()

#Input Generation
inp = randint(0,1023)
print("Randomized Input: ")
print(inp)
inp_b = inp.to_bytes(length=2, byteorder="little", signed=0)

#Ciphertext Generation
key = b'\x1a\xe0J\xb7\xfe\x18\x08>+\xd9\xb4\xb8,+n#\xef\xc1\x0b\xa2\xa3\x01\x8c\xf4\xd7\x17\xbf\xc9\xc0\x0c\xb0z'
cipher = ChaCha20_Poly1305.new(key=key)
ciphertext, tag = cipher.encrypt_and_digest(inp_b)
nnc = cipher.nonce

#socket variables
host = '127.0.0.1'
port = 12345
port1 = 12346
port2 = 12347
print(ciphertext)
print(tag)
print(nnc)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
    s1.connect((host,port))
    print('sending ciphertext...')
    s1.sendall(ciphertext)
    data = s1.recv(1024)
    print(data)
s1.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
    s2.connect((host,port1))
    print('sending tag...')
    s2.sendall(tag)
    data = s2.recv(1024)
    print(data)
s2.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s3:
    s3.connect((host,port2))
    print('sending nnc...')
    s3.sendall(nnc)
    data = s3.recv(1024)
    print(data)
s3.close()
  
Total_time = (time.time()-time_start)
print(Total_time)

#Decryption
#cipher_d = ChaCha20_Poly1305.new(key=key, nonce=nnc)
#plaintext_b = cipher_d.decrypt_and_verify(ciphertext,tag)
#plaintext = int.from_bytes(plaintext_b, byteorder="little", signed=0)
#
#print("Plaintext: ")
#print(plaintext)
