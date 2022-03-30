import paho.mqtt.client as mqtt 
import os
import redis
import sys

mqhost = os.environ['MOSQUITTO_HOST']
rhost = os.environ['REDIS_HOST']
rauth = os.environ['REDIS_AUTH']
stopic = os.environ['SENSOR_TOPIC']

def on_connect(client, userdata, flags, rc):
    print({"subscribed":"true","rc":str(rc)},file=sys.stderr)
    client.subscribe(stopic)

def on_message(client, userdata, msg):
    print({"topic":msg.topic,"payload":str(msg.payload)},file=sys.stderr)
    r = redis.StrictRedis(host=rhost,\
        port=6379,db=0,password=rauth,\
        decode_responses=True)
    r.rpush(stopic,msg.payload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqhost, 1883, 60)

client.loop_forever()
