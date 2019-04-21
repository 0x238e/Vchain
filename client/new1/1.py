from socket import *
import get

HOST ='localhost'

PORT = 12345

BUFFSIZE=2048

ADDR = (HOST,PORT)

def d():
    tctimeClient = socket(AF_INET,SOCK_STREAM)

    tctimeClient.connect(ADDR)

    while True:
        data = tctimeClient.recv(BUFFSIZE).decode()
        print(data)
        get.shot()
        data = get.eval()
        tctimeClient.send(data.encode())

    tctimeClient.close()

while True:
    try:
        d()
    except:
        pass