import json
import os
import time
import datetime
from checkConnection import *
input=""
ledStatus=0
os.system('sudo sh -c "echo none > /sys/class/leds/led0/trigger"')
template= {
    "time":"" , 
    "temperature":"",
    "light":"",  
    "humidity":"" ,
    "soilHumidity":""
}

def checkValidity():
    global input
    if (input[0]!="~" or input[-1]!="."):
        raise ValueError("Incorrect payload")
    else:
        measurementArray=(input[1:].split("~")[0]).split("-")
        checksumArray=(input[1:].split("~")[1]).split(".")
        if(int(measurementArray[0])^int(measurementArray[1])!=int(checksumArray[1]) or int(measurementArray[2])^int(measurementArray[3])!=int(checksumArray[2])):
            raise ValueError("Checksum failed")
        else:
            return measurementArray
def convertLight(analogValue):
    if analogValue<500:
        return 0
    elif analogValue>1000:
        return 100
    else:
        return (analogValue-500)/5
def convertHumid(analogValue):
    if analogValue>1000:
        return 0
    elif analogValue<100:
        return 100
    else:
        return (-analogValue+1000)/9
def fileHandler():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for files in os.listdir(dir_path):
        if files.endswith('.m'):
            try:
                c8ySend(files)
            except:
                pass
            os.remove(files)
def c8ySend(files):
    global input
    global ledStatus
    f=open(files,"r")
    input=f.read().strip()
    valueArray=checkValidity()
    template["time"]=files[:-2]
    template["temperature"]=int(valueArray[2])
    template["humidity"]=int(valueArray[3])
    template["soilHumidity"]=int(convertHumid(int(valueArray[1])))
    template["light"]=int(convertLight(int(valueArray[0])))
    payload=json.dumps(template)
    os.system("tedge mqtt pub tedge/measurements '"+payload+"'" )
while True:
    if (checkConnection()):
	    fileHandler()
        os.system('sudo sh -c "echo '+str(-ledStatus)+' > /sys/class/leds/led0/brightness"')
        ledStatus=~ledStatus
    time.sleep(1)
