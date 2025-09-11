// mBot (mCore) Ultrasonic Scanner
// Tries common RJ25 mappings for PORT_3 (D6/D7) and PORT_4 (D10/D11),
// and tries both TRIG/ECHO orders for each mapping.

struct Pair { int a; int b; const char* label; };
Pair combos[] = {
  {6, 7,  "PORT_3: TRIG=D6 ECHO=D7"},
  {7, 6,  "PORT_3: TRIG=D7 ECHO=D6"},
  {10, 11,"PORT_4: TRIG=D10 ECHO=D11"},
  {11, 10,"PORT_4: TRIG=D11 ECHO=D10"},
};

long usToCm(long us){ return us > 0 ? us/29/2 : 400; } // 400 = timeout/out-of-range

void setup(){
  Serial.begin(9600);
  Serial.println("mBot Ultrasonic Port/Pin Scanner");
}

long readOnce(int TRIG, int ECHO){
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long dur = pulseIn(ECHO, HIGH, 30000); // ~5m max; 30 ms timeout
  return usToCm(dur);
}

void loop(){
  for (auto &c : combos){
    long cm = readOnce(c.a, c.b);
    Serial.print(c.label);
    Serial.print("  ->  ");
    Serial.print(cm);
    Serial.println(" cm");
    delay(250);
  }
  Serial.println("---");
  delay(500);
}
