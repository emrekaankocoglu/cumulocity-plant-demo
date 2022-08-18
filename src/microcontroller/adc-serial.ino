
#include <Adafruit_Sensor.h>
#include <DHT.h>
DHT dht(12,DHT11);
void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(100);
  requestEvent();
}
void requestEvent(){
  char str[20];
  int light=analogRead(A0);
  delay(50);
  int soilHumid=analogRead(A2);
  delay(50);
  int airTemp=int(dht.readTemperature());
  int airHumid=int(dht.readHumidity());
  int checksumAnalog=light^soilHumid;
  int checksumDigital=airTemp^airHumid;
  String lightSensor= String(light,DEC);
  String humidSensor= String(soilHumid,DEC);
  String payload=String("~"+lightSensor+"-"+humidSensor+"-"+String(airTemp,DEC)+"-"+String(airHumid,DEC)+"~");
  payload.toCharArray(str,20);
  Serial.print("s");
  Serial.println(str);
  Serial.print(".");
  Serial.print(checksumAnalog);
  Serial.print(".");
  Serial.print(checksumDigital);
  Serial.println(".");
}
