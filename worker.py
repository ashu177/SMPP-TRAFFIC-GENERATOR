import smpplib
from smpplib import client
from multiprocessing import Process
import threading
import json
from RedisConn import RedisQueue
import RedisConn
import mysql.connector
import time
import random
import string

class workerClass:
    database = mysql.connector.connect(host="localhost",user="root",passwd="root",db="smpp")
    mycursor = database.cursor()
    red =RedisConn.getred()
    def randomMsg(self,stringlen = 160):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(stringlen))

    def sendBindTransceiver(self,client, system_id, password, system_type):
        print("Send bind trancv SystemID %s Password %s SystemType %s" % (system_id, password, system_type))
        try:
            client.bind_transceiver(system_id=system_id, password=password, system_type=system_type)
        
        except:
            print("sendBindTransceiver Exception occured")
            
        
    def connectSmppClient(self,ip, port):
        print("Connect to SMPP Client IP %s Port %d " % (ip, port))
        print("connect ")
        try:
            client = smpplib.client.Client(ip, port,1)
            client.connect()
        except:
            raise
        return client


    def sendShortMessage(self,client,data={}):
        dest_range=int(data["destinationAddressRange"].encode('utf-8'))
        dest_src=int(data["destinationAddress"].encode('utf-8'))
        src_range=int(data["sourceAddressRange"].encode('utf-8'))
        src_start=int(data["sourceAddress"].encode('utf-8'))
        key_pause=str(data["timeStamp"])+"_pause"
        key_stop=str(data["timeStamp"])+"_stop"
        global totMsg
        totMsg=dest_range*src_range
        print(totMsg)
        for src_add in range(src_start,src_range+src_start):
            for dest_add in range(dest_src,dest_range+dest_src):
                
                if(str(data["messageMethod"])=="randomMessage"):
                    data["shortMessage"]=workerClass().randomMsg(10)
        
                print(data["messageMethod"])
                print(data["shortMessage"])
                while workerClass().red.get(key_pause)=="1":
                    #print(workerClass().red.get(key),key)
                    print("pause")
                    time.sleep(10)
                while workerClass().red.get(key_stop)=="1":
                    return
                try:
                    pdu = client.send_message(source_addr_ton=int(data["sourceAddressTon"].encode('utf-8')),
                                        source_addr_npi=int(data["sourceAddressNpi"].encode('utf-8')),
                                        source_addr=str(src_add),
                                        dest_addr_ton=int(data["destinationAddressTon"].encode('utf-8')),
                                        dest_addr_npi=int(data["destinationAddressNpi"].encode('utf-8')),
                                        destination_addr=str(dest_add),
                                        short_message=data["shortMessage"].encode('utf-8'),
                                        registered_delivery=int(data["registeredDelivery"].encode('utf-8')),
                                        data_coding=int(data["dataCoding"].encode('utf-8')))

                    print("inside send msg ",str(src_add),str(dest_add))
                    data["msgSend"] = int(data["msgSend"])+1
                    print(data["msgSend"])
                    key = str(data["timeStamp"])+"_send"
                    print("key====="+key)
                    self.red.set(key,data["msgSend"])
            

                except:
                    raise
                    print("SendShortMessage exception occured")
                    
            print(data["msgSend"])
            print("SendShortMessage database")
            print(data["msgSend"])
            sql = "UPDATE smpptrafficmonitor SET msgSend = %s where timeStamp= %s"            
            val = (int(data["msgSend"]), str(data["timeStamp"]))
            workerClass().mycursor.execute(sql, val)
            workerClass().database.commit()

    def stop(self):
        print("stop fun")
        sql = "UPDATE smpptrafficmonitor SET ackRecv = %s,status =%s where timeStamp= %s"            
        val = (int(data["ackRecv"]) ,"1", str(data["timeStamp"]))
        workerClass().mycursor.execute(sql, val)
        workerClass().database.commit()
        
        try:
            
            client.unbind()
            client.disconnect()
        except Exception as e:
            print(e)
            print("Unbind exception occured")
        print("Send unbind")
        
    def getRadisData(self):
        global data
        q=RedisQueue('test')
        dataFromRedis=q.get()
        print(type(dataFromRedis))
        data=json.loads(dataFromRedis)
        print(type(data))
        return data
    
    def getResponse(self ,pdu, **kwargs):
        global totMsg
        key_stop=str(data["timeStamp"])+"_stop"
        print("got submitsm response", pdu.message_id)
        if(pdu.message_id):
            data["ackRecv"] = int(data["ackRecv"]) +1 
            #sql = "INSERT INTO smsAckReceive () VALUES (%s, %s , %s)"
            #val = (int(data["ackRecv"]) , pdu.message_id, str(data["timeStamp"]))
            #workerClass().mycursor.execute(sql, val)
            #workerClass().database.commit()
            
            key = str(data["timeStamp"])+"_recv"
            print("key====="+key)
            self.red.set(key,data["ackRecv"])
            print(data["ackRecv"])
            
        if(int(data["ackRecv"]) == int(data["msgSend"])  and workerClass().red.get(key_stop)=="1"):
            workerClass().stop()
            print(data["ackRecv"])
        if(int(data["ackRecv"]) == totMsg):
            workerClass().stop()
            print(data["ackRecv"])
            
        
    def start(self):
        print("INSIDE start")
        global client
        global totMsg
        global pdu,data

        
        
        data=workerClass().getRadisData()
        workerClass().red.set("time",data["timeStamp"])
        key_pause=str(data["timeStamp"])+"_pause"
        workerClass().red.set(key_pause,"0")
        key_stop=str(data["timeStamp"])+"_stop"
        workerClass().red.set(key_stop,"0")
        print(data["ip"])
        client =workerClass().connectSmppClient(data["ip"],(int)(data["portNumber"]))       
        try:
            workerClass().sendBindTransceiver(client, data["systemId"],data["password"],data["systemType"])         
        except Exception as e:
            print(e)  
              
        sendingMessageThread = threading.Thread(target=workerClass().sendShortMessage,  args=(client,data))       
        sendingMessageThread.start()
        sendingMessageThread.join()
        
        client.set_message_sent_handler(workerClass().getResponse)

        recevingMessageThread= threading.Thread(target=client.listen())        
        recevingMessageThread.start()
        
        recevingMessageThread.join()

    
def main():
    print("INSIDE MAIN")
    worker = workerClass()
    worker.start()

def wprocess():
    print("send message")
    p =Process(target=main)
    print("send message2")#to start a new message load
    p.start()
    p.join()
