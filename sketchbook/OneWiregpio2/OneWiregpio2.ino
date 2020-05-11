int rele1 = 12;
int rele2 = 11;

int incomingByte = 0;
int available = 0;

#include <OneWire.h> 
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2 
OneWire oneWire(ONE_WIRE_BUS); 

DallasTemperature sensors(&oneWire);
 
void setup(void) 
{ 
 pinMode(rele1, OUTPUT); 
 pinMode(rele2, OUTPUT); 
 Serial.begin(9600); 
 Serial.println("Dallas Temperature IC Control Library Demo"); 
 sensors.begin(); 

while (Serial.available () > 0){
    Serial.print("II received: ");
    Serial.println(Serial.read());
}

 
} 
void loop(void) 
{ 
 // call sensors.requestTemperatures() to issue a global temperature 
 // request to all devices on the bus 

/********************************************************************/
 Serial.print(" Requesting temperatures..."); 
 sensors.requestTemperatures(); // Send the command to get temperature readings 
 Serial.println("DONE"); 

/********************************************************************/
 Serial.print("Temperature uno is: "); 
 Serial.print(sensors.getTempCByIndex(0)); // Why "byIndex"?
 Serial.println("chau");
 Serial.print("Temperature dos is: "); 
 Serial.print(sensors.getTempCByIndex(1)); // Why "byIndex"? 
 Serial.println("chau");
 Serial.print("Temperature tres is: "); 
 Serial.print(sensors.getTempCByIndex(2)); // Why "byIndex"?
 Serial.println("chau");
 Serial.print("Temperature cuatro is: "); 
 Serial.print(sensors.getTempCByIndex(3)); // Why "byIndex"?
 Serial.println("chau");
 Serial.print("Temperature cinco is: "); 
 Serial.print(sensors.getTempCByIndex(4)); // Why "byIndex"?
 Serial.println("chau");
 Serial.print("Temperature seis is: "); 
 Serial.print(sensors.getTempCByIndex(5)); // Why "byIndex"?
 Serial.println("chau");
   // You can have more than one DS18B20 on the same bus.  
   // 0 refers to the first IC on the wire 
   delay(1000); 



available = Serial.available();
Serial.print("available: ");
Serial.println(available);
//H -> 72
//L -> 76

if (available > 0) {
   incomingByte = Serial.read();
   Serial.print("I received: ");
   Serial.println(incomingByte, DEC);
   
   if (incomingByte == 72) {
     Serial.println("Rele High!");
     digitalWrite(rele2, HIGH);
   }
   if (incomingByte == 76) {
    Serial.println("Rele Low!");
     digitalWrite(rele2, LOW);
   }

   while (Serial.available () > 0){
    Serial.print("II received: ");
    Serial.println(Serial.read());
}
} else {
  Serial.println("NOTHING AVAILABLE!!!");
}
}
