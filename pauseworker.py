import redis

red =redis.Redis("localhost")
red.set("pause","1")
