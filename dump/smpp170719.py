import smpplib
import sys
from multiprocessing import Process
import threading
import json
from RedisConn import RedisQueue

startIndex=0
totalMessages=1



def sendBindTransceiver(client, system_id, password, system_type):
    print("Send bind trancv SystemID %s Password %s SystemType %s" % (system_id, password, system_type))
    try:
        client.bind_transceiver(system_id=system_id, password=password, system_type=system_type)
       
    except:
        print("sendBindTransceiver Exception occured")

class connectWorker:   

    def connectSmppClient(self,ip, port):
        print("Connect to SMPP Client IP %s Port %d  %d" % (ip, port ,1))
        print("connect ")
        try:
        
            client = smpplib.client.Client(ip, port)
            
            # Print when obtain message_id
            client.set_message_sent_handler(
            lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
            client.set_message_received_handler(
            lambda pdu: sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id)))
            client.connect()
        except:
            raise
        return client


def sendShortMessage(client,totalMessages=''):
    msisdnList=data["destination_addr"]
    print("inside thread",msisdnList)
    try:
        for x in msisdnList:
            client.send_message(source_addr_ton=int(data["source_addr_ton"]),
                                source_addr_npi=int(data["source_addr_npi"]),
                                source_addr=data["source_addr"],
                                dest_addr_ton=int(data["dest_addr_ton"]),
                                dest_addr_npi=int(data["dest_addr_npi"]),
                                destination_addr=x,#data["destination_addr"],
                                short_message=data["short_message"],
                                registered_delivery=int(data["registered_delivery"]),
                                data_coding=int(data["data_coding"]))
            passData={"source_addr_ton":data["source_addr_ton"],
                      "source_addr_npi":data["source_addr_npi"],
                      "source_addr":data["source_addr"],
                      "dest_addr_ton":data["dest_addr_ton"],
                      "dest_addr_npi":data["dest_addr_npi"],
                      "destination_addr":x,
                      "short_message":data["short_message"],
                      "registered_delivery":data["registered_delivery"],
                      "data_coding":data["data_coding"]}
            
            string_data=json.dumps(passData)
            q=RedisQueue('test')
            q.put(string_data)


    except:
            print("SendShortMessage exception occured")
            


def sendUnbind(client):
    try:
        client.unbind()
        client.disconnect()
    except:
        print("Unbind exception occured")
    print("Send unbind")

def pushLoad(fromIndex, toIndex):
    #connecting to ip address
    connectWor=connectWorker()
    client = connectWor.connectSmppClient(data["ip"], int(data["port"]))
    #Bind Tranceiver
    try:
        sendBindTransceiver(client, data["system_id"],data["password"],data["system_type"])
    except Exception as e:
        print(e)
        
    #threads create to send messages    
    sendingMessageThread = threading.Thread(target=sendShortMessage,  args=(client,totalMessages)) 
    sendingMessageThread.start()
    
    #threads create to send messages
    recevingMessageThread= threading.Thread(target=client.listen()) 
    #start the threads
    
    recevingMessageThread.start()

    #jointhe threads
    sendingMessageThread.join()
    recevingMessageThread.join()
    
    sendUnbind(client)

def send_message(startIndex,totalMessages):
    print("send message")
    p =Process(target=pushLoad, args=(startIndex, totalMessages))#to start a new message load
    p.start()
    p.join()
    
    

if __name__=='__main__':


    send_message(startIndex,totalMessages)
