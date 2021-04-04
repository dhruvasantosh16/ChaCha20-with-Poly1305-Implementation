from Cryptodome.Cipher import ChaCha20_Poly1305
from Cryptodome.Random import get_random_bytes
from Cryptodome.Random.random import randint
from time import time_ns
import socket

#Input Generation
inp = randint(0,1023)
print("Randomized Input: ")
print(inp)
inp_b = inp.to_bytes(length=2, byteorder="little", signed=0)
print("In Bytes: ")
print(inp_b)

#Ciphertext Generation
key = b'\xe5@\xf0{\xee}Y\xe1\xb0`\xf1\xa8)\xb9^\x9cE\xe8\xa9X\xaal\xb2\x9eB\xdc\xc0\x1f\x161h\x04'
cipher = ChaCha20_Poly1305.new(key=key)
ciphertext, tag = cipher.encrypt_and_digest(inp_b)
nnc = cipher.nonce

print("Ciphertext: ")
print(ciphertext)
print("MAC: ")
print(tag)
#print("Nonce: ")
#print(cipher.nonce)

#Transmission Byte String
trans = b"".join([ciphertext,tag,nnc])
print(trans)

#Decryption
#cipher_d = ChaCha20_Poly1305.new(key=key, nonce=nnc)
#plaintext_b = cipher_d.decrypt_and_verify(ciphertext,tag)
#plaintext = int.from_bytes(plaintext_b, byteorder="little", signed=0)
#
#print("Plaintext: ")
#print(plaintext)


