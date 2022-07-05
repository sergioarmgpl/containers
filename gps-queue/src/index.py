import serial
import time
import string
import pynmea2
import os
import requests
import sys
import multiprocessing
import traceback
import json

from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
import json
from datetime import datetime

queue = []
traffic_events = []
cid = "cid-"+str(int(datetime.timestamp(datetime.now())))
device = os.environ['DEVICE']
ser = None

while True:
   try:
      ser = serial.Serial(device, baudrate=9600, timeout=1.0)
      print(os.environ['DEVICE']+" opened",file=sys.stderr)
      break
   except:
      print("Couldn't open "+os.environ['DEVICE'],file=sys.stderr)
      traceback.print_exc()

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
            print(data,file=sys.stderr)
            json_data = json.dumps(data) 
            f = open("/tmp/gps", "w")
            f.write(json_data)
            f.close()
            queue.append(data)
         else:
            print("Waiting for coordinates...",file=sys.stderr)
      except:
         print("No GPS data to send",file=sys.stderr)
