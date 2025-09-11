#include <MeMCore.h>

MeUltrasonicSensor ultrasonic(PORT_3); // Make sure the sensor is on port 3 or change this if needed

void setup() {
  Serial.begin(9600); // For reading distance values in Serial Monitor
  Serial.println("Ultrasonic Test Starting...");
}

void loop() {
  int distance = ultrasonic.distanceCm(); // read distance in cm

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(200); // update every 200ms
}
