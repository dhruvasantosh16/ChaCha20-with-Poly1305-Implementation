import subprocess
import time
for i in range(20):
    time.sleep(0.1)
    subprocess.call([r'D:\ChaCha20-with-Poly1305-Implementation\rec.bat'])
    time.sleep(1)
    subprocess.call([r'D:\ChaCha20-with-Poly1305-Implementation\tr.bat'])
