import serial
import time
import string
import pynmea2
import os
import requests
import sys

def redisCon():
   rhost = os.environ['REDIS_HOST']
   rauth = os.environ['REDIS_AUTH']
   return redis.StrictRedis(host=rhost,\
          port=6379,db=0,password=rauth,\
          decode_responses=True)

device = os.environ['DEVICE']
ser = serial.Serial(device, baudrate=9600, timeout=1.0)
cid = os.environ['CLIENT_ID']

while True:
   dataout = pynmea2.NMEAStreamReader()
   newdata = ser.readline().decode('utf-8')
   
   if newdata[0:6] == "$GPRMC":
      try:
         newmsg=pynmea2.parse(newdata)
         lat = newmsg.latitude
         lng = newmsg.longitude
         if lat != 0 and lng != 0:
            data = {'lat': lat,'lng':lng,'cid':cid}
            headers={"Content-Type":"application/json"}
            r = requests.post(os.environ['ENDPOINT']
              + f"/client/{cid}/position",json=data)
            print(str(r),file=sys.stderr)
            print(str(data),file=sys.stderr)
            r = redisCon()
            r.rpop("gps-queue",str(lat)+"|"+str(lng))
         else:
            print("Waiting for coordinates...",file=sys.stderr)
      except:
         print("No GPS data to send",file=sys.stderr)

