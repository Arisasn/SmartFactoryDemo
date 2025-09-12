#include <MeMCore.h>

// mBot motors (swap signs if yours turn opposite)
MeDCMotor motorLeft(M1);
MeDCMotor motorRight(M2);
MeBuzzer buzzer;

void drive(int left, int right, int ms){
  motorLeft.run(left);
  motorRight.run(-right); // right motor often needs opposite sign on mBot
  delay(ms);
  motorLeft.stop();
  motorRight.stop();
}

void setup() {
  Serial.begin(9600);
  buzzer.tone(1000, 200);
  delay(200);
}

void loop() {
  // Forward segment
  Serial.println("{\"car\":\"car1\",\"action\":\"forward\",\"ms\":1500}");
  drive(180, 180, 1500);

  // Short pause
  Serial.println("{\"car\":\"car1\",\"action\":\"pause\",\"ms\":250}");
  delay(250);

  // 90° turn (adjust ms if needed)
  Serial.println("{\"car\":\"car1\",\"action\":\"turn_right\",\"ms\":500}");
  drive(200, -200, 500);

  // Short pause
  Serial.println("{\"car\":\"car1\",\"action\":\"pause\",\"ms\":250}");
  delay(250);
}
