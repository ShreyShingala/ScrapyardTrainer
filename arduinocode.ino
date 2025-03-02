#define PIN2 2  // Define pin 2
void setup() {
    pinMode(PIN2, OUTPUT); 
    digitalWrite(PIN2, LOW);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available()) {      
        String signal = Serial.readStringUntil('\n'); 
        signal.trim();              

        if (signal == "boom") {
            digitalWrite(PIN2, HIGH);  
        } else {
            digitalWrite(PIN2, LOW); 
        }
    }
}
