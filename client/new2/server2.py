from socket import *
from time import ctime
import run

host = ''
port = 12345
buffsize = 2048
ADDR = (host,port)

tctime = socket(AF_INET,SOCK_STREAM)
tctime.bind(ADDR)
tctime.listen(3)

while True:
    print('Wait for connection ...')
    tctimeClient,addr = tctime.accept()
    print("Connection from :",addr)
    tctimeClient.send('start'.encode())
    while True:
        data = tctimeClient.recv(buffsize).decode()
        if not data:
            # break
            pass
        print(data)
        # input()
        run.update(data)
        tctimeClient.send('got'.encode())
    tctimeClient.close()

tctimeClient.close()
