import serial
import time
import datetime
import os
from checkConnection import *
ser = serial.Serial('/dev/ttyUSB0', 9600) #initiate serial connection-edit the ttyUSBxx to correct port (default for RPi)
read=""
input=ser.read()
count=0
connStatus=checkConnection()
timeInterval=5 #time interval between saved measurements when there is no connection to c8y (99 is the maximum)
for i in range(100):
    try:
        input.decode("utf-8")
    except:
        input=ser.read()
        continue
    break
for i in range(10):
    try:
        while(input.decode("utf-8"))!="s": #s is the start character for the payload from the serial connection
            input=ser.read()
        while (input.decode("utf-8"))=="s":
            read=""
            input=ser.read()
            while(input.decode("utf-8"))!="s":
                read=read+input.decode("utf-8")
                input=ser.read()
            if(count==100):
                connStatus=checkConnection() #check every 100 cycles the status of the c8y connection
                count=0
            if((not connStatus) and (count%timeInterval!=0)):
                print("No connection")
                time.sleep(1)
            else:
                ti=datetime.datetime.now().astimezone().replace(microsecond=0).isoformat() #create a measurement with the timestamp as the filename 
                f=open(ti+".temp","w") 
                f.write(read)
                f.close()
                base = os.path.splitext(ti+".temp")[0]
                os.rename(ti+".temp", base + ".m") #changing the file extension to avoid IO errors
                time.sleep(0.1)
            count+=1
    except:
        print("Transmission error, retrying...")
raise ConnectionError("Unreliable serial communication: Number of failed transmissions exceeded threshold")