import serial
import time
import string
import pynmea2
import os
import requests
import sys

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
         else:
            print("Waiting for coordinates...",file=sys.stderr)
      except:
         print("No GPS data to send",file=sys.stderr)

