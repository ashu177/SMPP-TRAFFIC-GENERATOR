import json
from RedisConn import RedisQueue

data = {"system_id" :"loadUser" , 
        "name": "test6",
        "password":"loadUser",
        "system_type":"qwerty",
        "port":"9999",
        "ip":"172.19.6.33",
        "source_addr_ton":"0",
        "source_addr_npi":"0",
        "source_addr":"5575",
        "source_addr_range":"100",
        "dest_addr_ton":"1",
        "dest_addr_npi":"1",
        "destination_addr":"919740555831",
        "destination_addr_range":"100",
        "short_message":"short message",
        "registered_delivery":"0",
        "data_coding":"0"}




class pushQueue:
    
    def push(self):
        print(data["name"])
        json_data=json.dumps(data)
        q=RedisQueue('test6')
        q.put(json_data)


        print(json_data)

        print(data["system_id"])

pushQueue().push()