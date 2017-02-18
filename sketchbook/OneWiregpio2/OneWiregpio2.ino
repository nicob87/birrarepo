int rele1 = 12;
int rele2 = 11;

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
 Serial.print("Temperature is: "); 
 Serial.print(sensors.getTempCByIndex(0)); // Why "byIndex"?  
   // You can have more than one DS18B20 on the same bus.  
   // 0 refers to the first IC on the wire 
   delay(1000); 
   //digitalWrite(rele1, HIGH);
   //delay(1000);
   //digitalWrite(rele2, HIGH);
   
   //delay(1000); 
   //digitalWrite(rele1, LOW);
   //delay(1000);
   //digitalWrite(rele2, LOW);
}
