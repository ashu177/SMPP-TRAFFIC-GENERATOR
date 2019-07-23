
import smpplib
import time
import random
import string
from multiprocessing import Process
import sys


randomMsgList = list()
totalMessages = 1
numThreads = 1

def randomMsg(stringlen = 160):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(stringlen))


def connectSmppClientMP(ip, port):
    
    print("Connect to SMPP Client IP %s Port %d  %d" % (ip, port ,1))
    #client_temp = None

    print("connect ")
    try:
       
        client = smpplib.client.Client(ip, port)
        client.connect()
    except:
        raise
   
    
    return client

def sendBindTransceiverMP(client, system_id, password, system_type):
    print("Send bind trancv SystemID %s Password %s SystemType %s" % (system_id, password, system_type))
    try:
        client.bind_transceiver(system_id=system_id, password=password, system_type=system_type)
       
    except:
        print("sendBindTransceiver Exception occured")
    
def sendShortMessage(client,om='', dm='', delvr='0', msg='test message', ston='0', snpi='0', dton='1', dnpi='1', dcs='0'):
    print("send short message")
    try:
        pdu=client.send_message(source_addr_ton=int(ston),
                            source_addr_npi=int(snpi),
                            source_addr=om,
                            dest_addr_ton=int(dton),
                            dest_addr_npi=int(dnpi),
                            destination_addr=dm,
                            short_message=msg,
                            registered_delivery=int(delvr),
                            data_coding=int(dcs))
        print("send msg done")
    except:
            print("SendShortMessage exception occured")
    
    #client._message_received()
    client.set_message_sent_handler(
        lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
    client.set_message_received_handler(
        lambda pdu: sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id)))
    #print(pdu.sequence)
    
      #  print("received")
def sendUnbind(client):
    try:
        client.unbind()
        client.disconnect()
    except:
        print("Unbind exception occured")
    print("Send unbind")
    
def pushLoadMP(fromIndex, toIndex):

    print("send message 2")
    client = connectSmppClientMP("172.19.6.33", 9999)
    
    sendBindTransceiverMP(client, "system_id", "password", "system_type")
    print("bind done")
    
    #for i in range len(randomMsgList)     
    for x in range(fromIndex, toIndex):
        try:
            print("sending short message")
            sendShortMessage(client,"55556", "919740555337", '1', "message body", '0', '0', '1', '1', '0')
            print("send short message")
        except Exception as e:
            print(e)
    print("%s Sent messages count: %d" % (time.time(), totalMessages))
    sendUnbind(client)

    print("Done")
    
        
    
    
    
def send_message(totalMessages):
    print("send message 1")
    p =Process(target=pushLoadMP, args=(0, totalMessages))
    p.start()
    p.join()
    
if __name__=='__main__':

    msg = '''Hi this is just a test'''
    print(msg)
    
    
    print("Random text list of %d Started" % (totalMessages))
    
    
    
    for i in range(totalMessages):
        text = randomMsg(159)
        randomMsgList.append(text)
    
    
    send_message(totalMessages)
    
    exit(0)