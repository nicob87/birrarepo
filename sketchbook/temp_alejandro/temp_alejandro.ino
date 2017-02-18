int sensorPin = 0;
int tempC, tempF;

void setup() {
  
Serial.begin(9600); 
Serial.println("Dallas Temperature IC Control Library Demo");

}


void loop() {
tempC = get_temperature(sensorPin);
tempF = celsius_to_fahrenheit(tempC);
delay(200);
Serial.print("la temperatura es: ");
Serial.println(tempC);
}


int get_temperature(int pin) {
// We need to tell the function which pin the sensor is hooked up to. We're using
// the variable pin for that above
// Read the value on that pin
int temperature = analogRead(pin);
// Calculate the temperature based on the reading and send that value back
float voltage = temperature * 5.0;
voltage = voltage / 1024.0;
return ((voltage - 0.5) * 100);
}



int celsius_to_fahrenheit(int temp) {
return (temp * 9 / 5) + 32;
}
