int S1_Pin = 5;
int S2_Pin = 4;
uint8_t receive_byte;
uint8_t received;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; 
  }
  pinMode(S1_Pin, OUTPUT);
  pinMode(S2_Pin, OUTPUT);
}

void loop() {
  /*
   * 0: Both off
   * 1: Relay 1
   * 2: Relay 2
   * 3: Both On
  */
  bool S1_value, S2_value;
  if (Serial.available() > 0) {
    // read the incoming byte:
    received = Serial.read();
    if (received == 'R'){
      int mask = 3;
      delay(200);
      Serial.print((int)(receive_byte&mask));
      }
    else if (received == '0' || received == '1' || received == '2' || received == '3'){
      receive_byte = received;
      S1_value = (bool)(receive_byte&(1<<0));
      S2_value = (bool)(receive_byte&(1<<1));
//      Serial.println(S1_value);
//      Serial.println(S2_value);
      digitalWrite(S1_Pin, S1_value);
      digitalWrite(S2_Pin, S2_value);
    }
  }
}
