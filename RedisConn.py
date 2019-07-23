import redis

class RedisQueue(object) :

    def __init__(self, name, namespace='queue'):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db= redis.Redis("localhost")
        self.key = '%s:%s' %(namespace, name)
    
    def put(self, item):
        self.__db.rpush(self.key, item)
        
    def get(self, block=True, timeout=None):
            """Remove and return an item from the queue. 
            If optional args block is true and timeout is None (the default), block
            if necessary until an item is available."""
            if block:
                item = self.__db.blpop(self.key, timeout=timeout)
            else:
                item = self.__db.lpop(self.key)
            if item:
                item = item[1]
            return item
    
def getred():
    red=redis.Redis("localhost")
    return red

#q.put('hello world')