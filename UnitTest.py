import unittest
import RedisConn
from Service import serviceClass
from worker import workerClass

data={
"systemId": "1", 
"password": "1", 
"systemType": "", 
"ip": "172.19.6.33", 
"portNumber": "9999",
"ackRecv": "0",
"dataCoding": "1",
"destinationAddress": "7678676",
"destinationAddressNpi": "1",
"destinationAddressRange": "10",
"destinationAddressTon": "1",
"messageMethod": "customMessage",
"msgSend": "0",
"registeredDelivery": "1",
"shortMessage": "sd",
"sourceAddress": "656",
"sourceAddressNpi": "0",
"sourceAddressRange": "10",
"sourceAddressTon": "0",
"timeStamp": 1564392706195
}

class TestStringMethods(unittest.TestCase):
    
    
    
    def test_conn(self):
        red=RedisConn.getred()       
        self.assertTrue(red.ping())
        print ("-------Redis Connection Passed---------")

    
    def test_ClientConnection(self):
        cli=workerClass().connectSmppClient("172.19.6.33",9999)
        #cli.bind_transceiver(system_id="1",password="1",system_type="1")
        #print(type(data))

        self.assertEquals(cli.poll(ignore_error_codes=""),None)
        #print("hellooo",cli.poll(ignore_error_codes="qwqe"))
        print ("-------Client Connection Passed---------")
    
    def test_db(self):
        res=serviceClass().pushDb(data)
        self.assertEquals(res,"True")
        tes="True"
        #print (res)
        res1=serviceClass().getData()
        if res1==None:
            tes="Fasle"
        self.assertEquals(tes,"True")
        print ("-------Database Test Passed---------")




if __name__ == '__main__': 
    unittest.main() 



