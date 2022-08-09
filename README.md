# Cumulocity Flower Demo
A demo project to integrate representative sensors for a "flower" -actually, a plant would be more appropriate, but the name is already there:)- to Cumulocity platform.
## Microcontroller
### Setup
An Arduino Uno/Nano can be used with LDR connected to pin A0 and the soil humidity sensor to pin A2 with a pull-up resistor or a potentiometer in between both their respective ground connections-close to 10k Ohms would be appropriate-. Connect it to the agent via USB or any serial-capable connection, and change the agent's device.py to use the appropriate port. You can get its connected serial port by executing the following command before and after the connection:
```
ls /dev/tty*
```
Any added file between executions will represent the connected serial port for the microcontroller.
### Communication
Any data "packet" that is sent by the microcontroller will look like this:
```
s~lightAnalog~soilHumidityAnalog~temperature~humidity~
.checksumAnalog.checksumDigital.
```
where "s" denotes the start of the transmission, "~" is the delimiter between sensor data, "." is the start and delimeter of checksums (simple xor of values) for lightAnalog (0-1023) and soidHumidityAnalog (0-1023), then temperature (digital, no conversion Celsius) and humidity (digital, direct percentages) respectively. With values differing in magnitude in analog and digital readings it was easier and more accurate to use and check seperate checksums for their values.
```
checksumAnalog=lightAnalog^soilHumidityAnalog
checksumDigital=temperature^humidity
```
Any failure in the transmission of the data "packet" -a bit flip, unstable connection etc.- will be caught by the agent, and will not be sent to Cumulocity. You can monitor the transmission by connecting the microcontroller to any serial monitor -e.g. your computer- to see whether the data sent is correct and sensor readings are in order.
## Agent
### Setup
Clone the repository, edit the agent.py as described in Microcontroller Setup section if needed, run the script start.sh on the same directory, and edit the URL in checkConnection.py to your tenant's URL. The systemd services ifdeviceconnector.service -serial connection- and ifdeviceagent.service -data agent- will already be configured and enabled to get them started at every startup.

Additionally, you can edit the variable timeInterval (*default 5s*) in device.py to determine the interval between two measurements stored -to be sent to Cumulocity afterwards- when there exists no Internet connection, and the interval it checks whether there is an Internet connection or not (time interval for this is *2 timeIntervals*)
