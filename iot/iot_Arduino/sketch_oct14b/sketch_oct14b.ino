#include <Servo.h>

Servo servo1;  // Servo connected to pin 11
Servo servo2;  // Servo connected to pin 10
Servo servo3;  // Servo connected to pin 9
Servo servo4;  // Servo connected to pin 6

void setup() {
  // Attach the servos to the respective pins
  servo1.attach(11);
  servo2.attach(10);
  servo3.attach(9);
  servo4.attach(6);

  // Set initial positions
  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);

  Serial.begin(9600);  // Start serial communication
  Serial.println("Enter 1, 2, 3, or 4 to move the corresponding servo.");
}

void loop() {
  if (Serial.available() > 0) {
    char input = Serial.read();  // Read the incoming serial data

    // Check which number is entered and move the corresponding servo to 180 degrees
    switch (input) {
      case '1':
        servo1.write(180);  // Move servo on pin 11 to 180 degrees
        Serial.println("Servo 1 moved to 180");
        delay(1000);
        servo1.write(0);
        Serial.println("Servo 1 moved to 0");
        break;
      case '2':
        servo2.write(90);  // Move servo on pin 10 to 180 degrees
        Serial.println("Servo 2 moved to 90");
        delay(1000);
        servo2.write(0);
        Serial.println("Servo 2 moved to 0");
        break;
      case '3':
        servo3.write(120);  // Move servo on pin 9 to 180 degrees
        Serial.println("Servo 3 moved to 180");
        delay(1000);
        servo3.write(0);
        break;
      case '4':
        servo4.write(50);  // Move servo on pin 6 to 180 degrees
        Serial.println("Servo 4 moved to 180");
        delay(1000);
        servo4.write(0);
        break;
      default:
        Serial.println("Invalid input, please enter 1, 2, 3, or 4.");
    }
  }
}
