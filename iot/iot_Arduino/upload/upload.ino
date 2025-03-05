int receivedValue = 0;  // Variable to store received value

void setup() {
  Serial.begin(9600);  // Initialize serial communication at 9600 baud rate
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming byte
    receivedValue = Serial.parseInt();  // Read integer value from serial
    Serial.print("Received value: ");
    Serial.println(receivedValue);  // Print received value to serial monitor
  }
}
