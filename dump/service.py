import json
from RedisConn import RedisQueue
from smpp170719 import pushLoad


data = {"system_id" :"loadUser" , 
        "password":"loadUser",
        "system_type":"qwerty",
        "port":"9999",
        "ip":"172.19.5.227",
        "source_addr_ton":"0",
        "source_addr_npi":"0",
        "source_addr":"55556",
        "source_addr_range":"2",
        "dest_addr_ton":"1",
        "dest_addr_npi":"1",
        "destination_addr":"919740555331",
        "destination_addr_range":"3",
        "short_message":"short message",
        "registered_delivery":"0",
        "data_coding":"0"}




if __name__=='__main__':
    json_data=json.dumps(data)
    q=RedisQueue('test')
    q.put(json_data)


    print(json_data)

    print(data["system_id"])
