// Raw HC-SR04-style read on mCore PORT_3 pins
const int TRIG = 8;   // PORT_3 TRIG
const int ECHO = 9;   // PORT_3 ECHO

long microsecondsToCm(long us){ return us / 29 / 2; }

void setup() {
  Serial.begin(9600);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  digitalWrite(TRIG, LOW);
  delay(50);
  Serial.println("Raw ultrasonic test on PORT_3 (D8/D9)...");
}

void loop() {
  // trigger 10us pulse
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  long duration = pulseIn(ECHO, HIGH, 30000); // timeout ~30ms (~5m)
  long cm = duration ? microsecondsToCm(duration) : 400; // 400 = out of range
  Serial.print("Distance: "); Serial.print(cm); Serial.println(" cm");
  delay(200);
}
