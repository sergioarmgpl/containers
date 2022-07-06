import os
import redis
import sys
import time

rhost = os.environ['REDIS_HOST']
rauth = os.environ['REDIS_AUTH']
delay = int(os.environ['DELAY'])
r = redis.StrictRedis(host=rhost,\
          port=6379,db=0,password=rauth,\
          decode_responses=True)

while True:
    objects = r.zrange("traffic",0,-1)
    for obj in objects:
        print(obj,file=sys.stderr)
        print(r.exists(f"object:{obj}:data"),file=sys.stderr)
        if not r.exists(f"object:{obj}:data"):
            r.zrem("traffic",obj)
            print({"deleted":obj},file=sys.stderr)
    time.sleep(delay)