#include <MeMCore.h>

// Port numbers depend on your wiring
MeDCMotor motorLeft(M1);
MeDCMotor motorRight(M2);
MeUltrasonicSensor ultrasonic(PORT_3);
MeBuzzer buzzer;

void setup() {
  Serial.begin(9600); // For distance logging
}

void loop() {
  // Move forward
  motorLeft.run(100);
  motorRight.run(-100);  // negative reverses direction
  delay(1000);

  // Stop
  motorLeft.stop();
  motorRight.stop();

  // Beep
  buzzer.tone(1000, 500);

  // Measure distance
  int distance = ultrasonic.distanceCm();
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(1000); // Pause before repeating
}
