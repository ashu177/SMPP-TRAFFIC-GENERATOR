import smpplib
from smpplib import client
from multiprocessing import Process
import threading
import json
from RedisConn import RedisQueue
import RedisConn
import mysql.connector
import time



class workerClass:
    database = mysql.connector.connect(host="localhost",user="root",passwd="root",db="smpp")
    mycursor = database.cursor()
    red =RedisConn.getred()

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

        global totMsg,msgSend
        totMsg=dest_range*src_range
        print(data)
        for src_add in range(src_start,src_range+src_start):
            for dest_add in range(dest_src,dest_range+dest_src):
                while workerClass().red.get("pause")=="1":
                    print("pause")
                    time.sleep(10)
                while workerClass().red.get("stop")=="1":
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
                    #print(type(int(data["source_addr_ton"])))
                    print(pdu.sequence)
                    print("inside send msg ",str(src_add),str(dest_add))
                    msgSend = msgSend+1
                    workerClass().red.set("msgSend",msgSend)
                        
            

                except:
                    raise
                    print("SendShortMessage exception occured")
            

    def stop(self):
        print("stop fun")
        
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
        global count,totMsg,ackRecv
        print("got submitsm response", pdu.message_id)
        if(pdu.message_id):
            ackRecv = ackRecv +1 
            workerClass().red.set("AckRecv",ackRecv)
            sql = "INSERT INTO smAck (id, Ack) VALUES (%s, %s)"
            val = (ackRecv , pdu.message_id)
            workerClass().mycursor.execute(sql, val)
            workerClass().database.commit()
        if(ackRecv == totMsg):
            workerClass().stop()
            print(ackRecv)
        
    def start(self):
        print("INSIDE start")
        global client
        global ackRecv,msgSend
        global totMsg
        global pdu,data
        ackRecv = 0
        totMsg = 0
        msgSend = 0
        
        workerClass().red.set("pause","0")
        workerClass().red.set("stop","0")
        workerClass().red.set("AckRecv","0")
        workerClass().red.set("msgSend","0")
        data=workerClass().getRadisData()
        client =workerClass().connectSmppClient(data["ip"],(int)(data["portNumber"]))        #connecting to ip address

        try:
            workerClass().sendBindTransceiver(client, data["systemId"],data["password"],data["systemType"])         #Bind Tranceiver
        except Exception as e:
            print(e)  
              
        sendingMessageThread = threading.Thread(target=workerClass().sendShortMessage,  args=(client,data))         #threads create to send messages 
        sendingMessageThread.start()
        sendingMessageThread.join()
        
        client.set_message_sent_handler(workerClass().getResponse)

        recevingMessageThread= threading.Thread(target=client.listen())         #thread listining the client
        recevingMessageThread.start()
        
        recevingMessageThread.join()

    
def main():
    print("INSIDE MAIN")
    worker = workerClass()
    worker.start()
    worker.stop()
        
if __name__=='__main__':
    print("send message")
    p =Process(target=main)#to start a new message load
    p.start()
    p.join()
