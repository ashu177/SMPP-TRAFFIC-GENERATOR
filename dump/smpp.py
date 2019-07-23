import smpplib
import time
import random
import string
import threading
from multiprocessing import Process
import os

clients = []
randomMsgList = []
totalMessages = 1
numThreads = 1

    os.fo
def randomMsg(stringlen = 160):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(stringlen))

class connection:

    def connectSmppClient(self,ip, port, numConnections = 1):
        global clients
        print("Connect to SMPP Client IP %s Port %d NumConnections %d" % (ip, port, numConnections))
        #client_temp = None

        for i in range(numConnections):
            print("connect %d" % (i,))
            try:
                client_temp = smpplib.client.Client(ip, port)
                client_temp.connect()
                clients.append(client_temp)
            except:
                raise

def sendBindTransceiver(system_id, password, system_type):
    print("Send bind trancv SystemID %s Password %s SystemType %s" % (system_id, password, system_type))
    for client in clients:
        try:
            client.bind_transceiver(system_id=system_id, password=password, system_type=system_type)
        except:
            print("sendBindTransceiver Exception occured")
            clients.remove(client)

def sendShortMessage(om='', dm='', delvr='0', msg='text msg', ston='0', snpi='0', dton='1', dnpi='1', dcs='0'):
    global clients
    for client in clients:
        try:
            client.send_message(source_addr_ton=int(ston),
                        source_addr_npi=int(snpi),
                        source_addr=om,
                        dest_addr_ton=int(dton),
                        dest_addr_npi=int(dnpi),
                        destination_addr=dm,
                        short_message=msg,
                        registered_delivery=int(delvr),
                        data_coding=int(dcs)
                        )
            

                        
        except Exception as e:
            print("SendShortMessage exception occured")
            print(e)
    #print("Send short message")

def sendUnbind():
    global clients
    try:
        for client in clients:
            client.unbind()
            client.disconnect()
    except:
        print("Unbind exception occured")
    print("Send unbind")


def pushLoad(fromIndex, toIndex):
    #connectSmppClient("172.19.5.227", 6666, 1)
    for x in range(fromIndex, toIndex):
        try:
            #print("Send short message %d" % (i,))
            connection.connectSmppClient("192.168.60.1", 9999, 1)
            sendBindTransceiver("loaduser1", "load1", "load1")
            sendShortMessage("55556", "919740555337", '1', randomMsgList[i], '0', '0', '1', '1', '0')
          #  print("i am here")
            
        except Exception as e:
            print(e)
    
        time.sleep(0.001)    

def threadLoad(numThreads, totalMessages):
    
    startRange = 0
    
    if __name__=='__main__':
        p=Process(target=pushLoad, args=(startRange,totalMessages))
        p.start()
        p.join()
        print("finished")

        
        #loadThread.join()


#__main_()__

#connectSmppClient("192.168.221.1", 3000, 1)


msg = '''Hi this is just a test'''
msg_long = '''The National Green Tribunal (NGT) on Thursday passed a slew of directions to rejuvenate the Ganga. It declared as No-Development Zone an area of 100 metres from the edge of the river between Haridwar and Unnao and prohibited the dumping of waste within 500 metres from the river.
    A bench of the NGT also declared that a penalty of 50,000 as environment compensation charge would be imposed on anyone who dumped waste in the river.
    The NGT directed the Uttar Pradesh and Uttarakhand governments to formulate guidelines for religious activities on the ghats of the Ganga or its tributaries.'''
print(msg)


time.sleep(.5)
text = ""

print("%s Random text list of %d Started" % (time.time(), totalMessages))

for i in range(totalMessages):
    text = randomMsg(159)
    randomMsgList.append(text)

print("%s Random text list of %d created" % (time.time(), totalMessages))

print("%s Sending messages count: %d" % (time.time(), totalMessages))

threadLoad(numThreads, totalMessages)

print("%s Sent messages count: %d" % (time.time(), totalMessages))
print("sending unbind")
sendUnbind()

print("Done")
exit(0)