from Cryptodome.Cipher import ChaCha20_Poly1305
import socket
import time
import math
import os
file1 = open('timingdatareceive.txt', 'a')
start_time = time.time()

def sock(s, *args):
    host = ''
    port = 12345
    port1 = 12346
    port2 = 12347
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.bind((host,port))
    s2.bind((host,port1))
    s3.bind((host,port2))
    s1.listen()
    s2.listen()
    s3.listen()
    c1, addr1 = s1.accept()
    c2, addr2 = s2.accept()
    c3, addr3 = s3.accept()
    if s == "send":
        data1 = args[0]
        data2 = args[1]
        data3 = args[2]
        with c1:
            #print("sending", data1)
            c1.sendall(data1)
            #ack = c1.recv(1024)
            #print(ack)
            s1.close()

        
        with c2:
            #print("sending", data2)
            c2.sendall(data2)
            #ack2 = c2.recv(1024)
            #print(ack2)
            s2.close()
        
        
        with c3:
            #print("sending", data3)
            c3.sendall(data3)
            #ack3 = c3.recv(1024)
            #print(ack3)
            s3.close()

    else:
        with c1:
            rdata1 = c1.recv(2000)
            #print('received', rdata1)
            #c1.sendall(b"acknowledged")
            s1.close()

        with c2:
            rdata2 = c2.recv(2000)
            #print('received', rdata2)
            #c2.sendall(b"acknowledged")
            s2.close()

        with c3:
            rdata3 = c3.recv(2000)
            #print('received', rdata3)
            #c3.sendall(b"acknowledged")
            s3.close()
            return rdata1, rdata2, rdata3
 
def dec(data1, data2, data3):
    key = b'\x1a\xe0J\xb7\xfe\x18\x08>+\xd9\xb4\xb8,+n#\xef\xc1\x0b\xa2\xa3\x01\x8c\xf4\xd7\x17\xbf\xc9\xc0\x0c\xb0z'
    cipher = ChaCha20_Poly1305.new(key=key, nonce=data3)
    plaintext_b = cipher.decrypt(data1)
    cipher.verify(data2)
    plaintext = int.from_bytes(plaintext_b, byteorder="little",signed=0)
    print("Randomized input: ", plaintext)
    return plaintext

def calc(plaintext):
    plaintext = plaintext ** (1/3)
    angle = math.floor(plaintext*10)
    #print("Angle of Servo: ",angle)
    angle_b = angle.to_bytes(length=2, byteorder="little", signed=0)
    return angle_b
    

def enc(angle_b):
    key = b'\x1a\xe0J\xb7\xfe\x18\x08>+\xd9\xb4\xb8,+n#\xef\xc1\x0b\xa2\xa3\x01\x8c\xf4\xd7\x17\xbf\xc9\xc0\x0c\xb0z'
    cipher = ChaCha20_Poly1305.new(key=key)
    ciphertext_r, tag_r = cipher.encrypt_and_digest(angle_b)
    nnc_r = cipher.nonce
    return ciphertext_r, tag_r, nnc_r

def main():
    data1, data2, data3 = sock("r")
    plaintext = dec(data1, data2, data3)
    angle_b = calc(plaintext)
    ciphertext_r, tag_r, nnc_r = enc(angle_b)
    sock("send", ciphertext_r, tag_r, nnc_r)
    

if __name__ == "__main__":
    main()

Total_time = (time.time()- start_time)
#print(Total_time)

file1.write(str(Total_time) + "\n")
file1.close()

#os.system('cmd /k')
