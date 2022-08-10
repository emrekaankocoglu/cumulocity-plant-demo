# Cumulocity Flower Demo
A demo project to integrate representative sensors for a "flower" -actually, a plant would be more appropriate, but the name is already there:)- to Cumulocity platform.
## Microcontroller
### Setup
An Arduino Uno/Nano can be used with a DHT11 -or some similar digital temperature sensor- on pin D12,  LDR connected to pin A0 and the soil humidity sensor to pin A2 with a pull-up resistor or a potentiometer in between both their respective ground connections-close to 10k Ohms would be appropriate-. Download DHT Library by Adafruit for Arduino from the Library Manager of Arduino IDE, connect the Arduino to your computer and upload the sketch in the microcontroller folder with Arduino IDE. Connect it to the agent via USB or any serial-capable connection, and change the agent's device.py to use the appropriate port. You can get its connected serial port by executing the following command before and after the connection:
```
ls /dev/tty*
```
Any added line between executions will represent the connected serial port for the microcontroller.
### Communication
Any data "packet" that is sent by the microcontroller will look like this:
```
s~lightAnalog~soilHumidityAnalog~temperature~humidity~
.checksumAnalog.checksumDigital.
```
where "s" denotes the start of the transmission, "~" is the delimiter between sensor data, "." is the start and delimeter of checksums (simple xor of values) for lightAnalog (0-1023) and soidHumidityAnalog (1023-0), then temperature (digital, no conversion Celsius) and humidity (digital, direct percentages) respectively. With values differing in magnitude in analog and digital readings it was easier and more accurate to use and check seperate checksums for their values.
```
checksumAnalog=lightAnalog^soilHumidityAnalog
checksumDigital=temperature^humidity
```
Any failure in the transmission of the data "packet" -a bit flip, unstable connection etc.- will be caught by the agent, and will not be sent to Cumulocity. You can monitor the transmission by connecting the microcontroller to any serial monitor -e.g. your computer- to see whether the data sent is correct and sensor readings are in order.
## Agent
### Setup
Clone the repository, edit the agent.py as described in Microcontroller Setup section if needed, run the script start.sh on the same directory, and edit the URL in checkConnection.py to your tenant's URL. The systemd services ifdeviceconnector.service -serial connection- and ifdeviceagent.service -data agent- will already be configured and enabled to get them started at every startup. The light will blink green whenever a transmission is tried on the agent side to Cumulocity.
### Configuration
Although they can also be calibrated with the potentiometer connected to analog sensors, one can also change the interval and values of the converted sensor data to Cumulocity in the convertLight and convertHumid blocks of the agent.py. The algorithm is pretty self-explanatory, but keep in mind that they are percentages -not necessarily, but the default is this-, and soil humidity sensor will output 1023 as plain dry, and 0 as it gets more moist, which is inverse to the light where 1023 is the brighest.
Additionally, you can edit the variable timeInterval (*default 5s*) in device.py to determine the interval between two measurements stored -to be sent to Cumulocity afterwards- when there exists no Internet connection, and the interval it checks whether there is an Internet connection or not (time interval for this is *2 timeIntervals*)
### Troubleshooting
Make sure you followed the setup fully. The first step with any problem, is actually unplug every connection to the agent, and plug it back in. With the restart, everything should be reinitialized which solves %90 of the problems:)
#### No data is sent to Cumulocity
##### No blink -light is solid or gone-
The agent device probably doesn't have the connection to the Internet. Make sure it does, if it does, then a failure repeated too many times. Have it restarted. If it still does not work, follow service troubleshooting and microcontroller troubleshooting steps.
##### Blink, but no data sent
Take a look at the agent directory. If you notice files with .m or .temp extensions are created, try to look at their contents to check if they fit to the format in the Communication section, and the checksums are correct. If it does not comply, try the microcontroller troubleshooting steps. If it does, run the following:
```
sudo tedge mqtt sub tedge/errors
```
This will show any transmission errors with Cumulocity's MQTT service. If there is any, there is probably a misconfiguration of thin-edge.io. Try to run start.sh again, or follow the troubleshooting steps on thin-edge.io's guide.
If there are no files with .m or .temp being created and deleted, check service troubleshooting steps with the emphasis on ifdevicecontroller service.
#### Data sent to Cumulocity is inaccurate
Follow microcontroller troubleshooting steps. Make sure you calibrated the analog sensors as you like, and edited the conversion block of agent.py correctly if you have done so. If no fault there, and the values are exactly as you expect, try to get the measurements with deviceID from Cumulocity's REST API to see if you can spot the problem.
#### Microcontroller Troubleshooting
