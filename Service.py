import requests
import json
from flask import Flask, request, jsonify
from multiprocessing import Process
from RedisConn import RedisQueue
from worker import workerClass
import redis
import yaml
from flask_cors import CORS
import logging
import worker

app = Flask(__name__)
CORS(app)

class serviceClass:
    
    def reciveMeaage(self, content):
        logging.info("Json Received")
        logging.info("pushing into Redis Queue")
        print ("content",content)
        self.push(content)
        #print request
        return jsonify({"Response code" : "00"})
        #return jsonify(response)

   

    def push(self,data):
        #print(data["name"])
        print("data=====",data)
        json_data=json.dumps(data)
        q=RedisQueue('test')
        q.put(json_data)
        

        worker.main()

        print(json_data)

       # print(data["system_id"])
    
    def start(self, content):
      print("hello")
      return serviceClass().reciveMeaage(content)

@app.route('/reciveMessage', methods=['GET', 'POST'])  
def main():
    service = serviceClass()
    print("hrll")
    return service.start(request.json)

if __name__ == '__main__':
    print("Service Started")
    p = Process(target = main)
    p.start()
    p.join()
    app.run(host="0.0.0.0",port=5000)
        