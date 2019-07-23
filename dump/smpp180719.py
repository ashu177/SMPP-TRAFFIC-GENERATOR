import smpplib
import sys
from multiprocessing import Process
import threading
import json
from RedisConn import RedisQueue


startIndex=0
totalMessages=1
count=0

#print(data1["source_addr"])

class Worker:
    
    def sendBindTransceiver(self,client, system_id, password, system_type):
        print("Send bind trancv SystemID %s Password %s SystemType %s" % (system_id, password, system_type))
        try:
            client.bind_transceiver(system_id=system_id, password=password, system_type=system_type)
        
        except:
            print("sendBindTransceiver Exception occured")



        
    def connectSmppClient(self,ip, port):
        global count
        print("Connect to SMPP Client IP %s Port %d  %d" % (ip, port ,1))
        print("connect ")
        #count=0
        try:
        
            client = smpplib.client.Client(ip, port)
            client.connect()
                
            # Print when obtain message_id
            
        except:
            raise
        return client
    
    def getResponse(self,pdu, **kwargs):
        global count
        print("got submitsm response %d", pdu.message_id)
        if(pdu.message_id):
            count=count+1
        
        if(count==10):
            print "hello"
            Worker().sendUnbind(Worker().connectSmppClient.client)
        #print(count)
        
        
        #print(type(count))
    def sendShortMessage(self,client,totalMessages='',data={}):
        #string_data=json.dumps(data)
        dest_range=int(data["destination_addr_range"].encode('utf-8'))
        dest_src=int(data["destination_addr"].encode('utf-8'))
        src_range=int(data["source_addr_range"].encode('utf-8'))
        src_start=int(data["source_addr"].encode('utf-8'))

        print("inside shore",dest_range,dest_src,src_range,src_range)
        #source_addr_List=range(int(data["source_addr"]),int(data["source_addr"])+int(data["source_addr_range"]))
        #print(source_addr_List)
        #msisdnList=data["destination_addr"]
       # print("inside thread",msisdnList)
        try:
        #for x in source_addr_List:
            for x in range(src_start,src_range+src_start):
                for y in range(dest_src,dest_range+dest_src):
                    #print(x,y)
                    client.send_message(source_addr_ton=int(data["source_addr_ton"]),
                                        source_addr_npi=int(data["source_addr_npi"]),
                                        source_addr=str(x),
                                        dest_addr_ton=int(data["dest_addr_ton"]),
                                        dest_addr_npi=int(data["dest_addr_npi"]),
                                        destination_addr=str(y),
                                        short_message=data["short_message"],
                                        registered_delivery=int(data["registered_delivery"]),
                                        data_coding=int(data["data_coding"]))
                #print(x)

        except:
            print("SendShortMessage exception occured")
            



    def sendUnbind(self,client):
        print "------"
        try:
            client.unbind()
            client.disconnect()
        except:
            print("Unbind exception occured")
        print("Send unbind")



    def pushLoad(self,fromIndex, toIndex):
        global count
        #connecting to ip address
        q=RedisQueue('test')
        dataFromRedis=q.get()

        data=json.loads(dataFromRedis)
        print(data["ip"])
        print("i am herr")
        client =Worker().connectSmppClient(data["ip"],(int)(data["port"]))
        #Bind Tranceiver
        try:
            Worker().sendBindTransceiver(client, data["system_id"],data["password"],data["system_type"])
        except Exception as e:
            print(e)
        
        
        
            
        #treads create to send messages    
        sendingMessageThread = threading.Thread(target=Worker().sendShortMessage,  args=(client,totalMessages,data)) 
        sendingMessageThread.start()
        client.set_message_sent_handler(Worker().getResponse)
            #
        client.set_message_received_handler(
            lambda pdu: sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id)))
        
        #print("count=",count)
        
        
        #threads create to send messages
        recevingMessageThread= threading.Thread(target=client.listen()) 
        #start the threads
        
        recevingMessageThread.start()

        #jointhe threads
        sendingMessageThread.join()
        recevingMessageThread.join()
        #print("count",count)
        Worker().sendUnbind(client)

def send_message(startIndex,totalMessages):
    print("send message")
    p =Process(target=Worker().pushLoad, args=(startIndex, totalMessages))#to start a new message load
    p.start()
    p.join()
    

    

if __name__=='__main__':



    send_message(startIndex,totalMessages)
    
