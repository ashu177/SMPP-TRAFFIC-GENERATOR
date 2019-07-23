from threading import Thread
import socket
#import smppProcess
#from smppProcess import connectSmppClientMP
import smpplib
s=socket.socket()
port=int("9999")
s.connect(('172.19.6.33',port))
s.accept()
#client=connectSmppClientMP("192.168.0.102", 9999)
#t = Thread(target=client.listen)
#t.start()