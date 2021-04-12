from Cryptodome.Cipher import ChaCha20_Poly1305
from Cryptodome.Random import get_random_bytes
from Cryptodome.Random.random import randint  
import time
import socket

#Timing Start
time_start = time.time()

#Input Generation
  
def input():
    inp = randint(0,1023)
    print("Randomized Input: ")
    print(inp)
    inp_b = inp.to_bytes(length=2, byteorder="little", signed=0)
    return inp_b

#Ciphertext Generation
  
def gen(inp_b):
    key = b'\x1a\xe0J\xb7\xfe\x18\x08>+\xd9\xb4\xb8,+n#\xef\xc1\x0b\xa2\xa3\x01\x8c\xf4\xd7\x17\xbf\xc9\xc0\x0c\xb0z'
    cipher = ChaCha20_Poly1305.new(key=key)
    ciphertext, tag = cipher.encrypt_and_digest(inp_b)
    nnc = cipher.nonce
    return ciphertext, tag, nnc
  
def sock(s, *args):
    host = '127.0.0.1'
    port = 12345
    port1 = 12346
    port2 = 12347
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((host,port))
    s2.connect((host,port1))
    s3.connect((host,port2))
    
    if s == "send":
        data1 = args[0]
        data2 = args[1]
        data3 = args[2]
        print("sending", data1)
        s1.sendall(data1)
        ack = s1.recv(2000)
        print(ack)

        print("sending", data2)
        s2.sendall(data2)
        ack = s2.recv(2000)
        print(ack)

        print("sending", data3)
        s3.sendall(data3)
        ack = s3.recv(2000)
        print(ack)

    else:
        rdata1 = s1.recv(2000)
        print("recieved", rdata1)
        s1.sendall(b"acknowledged")
        
        rdata2 = s2.recv(2000)
        print("received", rdata2)
        s2.sendall(b"acknowledged")

        rdata3 = s3.recv(2000)
        print("received", rdata3)
        s3.sendall(b"acknowledged")
        return rdata1, rdata2, rdata3

def main():
    inp_b = input()
    ciphertext, tag, nnc = gen(inp_b)
    sock("send",ciphertext, tag, nnc)
    ciphertext_r, tag_r, nnc_r = sock("r")
    print(ciphertext_r, tag_r, nnc_r)
    
if __name__ == "__main__":
    main()
  
Total_time = (time.time()-time_start)
print(Total_time)

#Decryption
#cipher_d = ChaCha20_Poly1305.new(key=key, nonce=nnc)
#plaintext_b = cipher_d.decrypt_and_verify(ciphertext,tag)
#plaintext = int.from_bytes(plaintext_b, byteorder="little", signed=0)
#
#print("Plaintext: ")
#print(plaintext)
