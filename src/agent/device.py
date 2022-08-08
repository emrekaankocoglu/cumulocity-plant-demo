import serial
import time
import datetime
import os
from checkConnection import *
ser = serial.Serial('/dev/ttyUSB0', 9600)
read=""
input=ser.read()
count=0
connStatus=checkConnection()
for i in range(100):
    try:
        input.decode("utf-8")
    except:
        input=ser.read()
        continue
    break
for i in range(10):
    try:
        while(input.decode("utf-8"))!="s":
            input=ser.read()
        while (input.decode("utf-8"))=="s":
            read=""
            input=ser.read()
            while(input.decode("utf-8"))!="s":
                read=read+input.decode("utf-8")
                input=ser.read()
            if(count==100):
                connStatus=checkConnection()
                count=0
            if((not connStatus) and (count%5!=0)):
                continue
            else:
                ti=datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
                f=open(ti+".temp","w")
                f.write(read)
                f.close()
                base = os.path.splitext(ti+".temp")[0]
                os.rename(ti+".temp", base + ".m")
                time.sleep(0.1)
            count+=1
    except:
        print("Transmission error, retrying...")
raise ConnectionError("Unreliable serial communication: Number of failed transmissions exceeded threshold")