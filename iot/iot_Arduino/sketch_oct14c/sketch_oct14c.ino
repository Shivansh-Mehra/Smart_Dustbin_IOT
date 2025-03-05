#include <Servo.h>

// Servo definitions
Servo servo1;  // Servo connected to pin 11
Servo servo2;  // Servo connected to pin 10
Servo servo3;  // Servo connected to pin 9
Servo servo4;  // Servo connected to pin 6

// Ultrasonic sensor definitions
const int trigPin = 3;   // Pin connected to the Trigger pin of the ultrasonic sensor
const int echoPin = 2;   // Pin connected to the Echo pin of the ultrasonic sensor
long duration;           // Variable for the duration of the sound wave travel
int distance;            // Variable for the calculated distance

void setup() {
  // Attach the servos to the respective pins
  servo1.attach(11);
  servo2.attach(10);
  servo3.attach(9);
  servo4.attach(6);

  // Set initial positions of servos
  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);

  // Initialize pins for the ultrasonic sensor
  pinMode(trigPin, OUTPUT);  // Set the Trigger pin as output
  pinMode(echoPin, INPUT);   // Set the Echo pin as input

  Serial.begin(9600);  // Start serial communication
  Serial.println("Enter 1, 2, 3, 4 to move the corresponding servo, or 5 to read distance.");
}

void loop() {
  if (Serial.available() > 0) {
    char input = Serial.read();  // Read the incoming serial data

    // Check which number is entered and perform the corresponding action
    switch (input) {
      case '1':
        servo1.write(180);  // Move servo on pin 11 to 180 degrees
        Serial.println("Servo 1 moved to 180");
        delay(1000);
        servo1.write(0);    // Move servo back to 0 degrees
        Serial.println("Servo 1 moved to 0");
        break;

      case '2':
        servo2.write(90);  // Move servo on pin 10 to 90 degrees
        Serial.println("Servo 2 moved to 90");
        delay(1000);
        servo2.write(0);    // Move servo back to 0 degrees
        Serial.println("Servo 2 moved to 0");
        break;

      case '3':
        servo3.write(120);  // Move servo on pin 9 to 120 degrees
        Serial.println("Servo 3 moved to 120");
        delay(1000);
        servo3.write(0);    // Move servo back to 0 degrees
        Serial.println("Servo 3 moved to 0");
        break;

      case '4':
        servo4.write(120);   // Move servo on pin 6 to 50 degrees
        Serial.println("Servo 4 moved to 50");
        delay(1000);
        servo4.write(0);    // Move servo back to 0 degrees
        Serial.println("Servo 4 moved to 0");
        break;

      case '5':
        // Ultrasonic distance measurement
        digitalWrite(trigPin, LOW);  // Clear the trigger pin
        delayMicroseconds(2);

        // Send a 10us HIGH pulse to the trigger pin to start measurement
        digitalWrite(trigPin, HIGH);
        delayMicroseconds(10);
        digitalWrite(trigPin, LOW);

        // Read the echo pin and calculate the time it takes for the echo to return
        duration = pulseIn(echoPin, HIGH);

        // Calculate the distance in centimeters
        distance = duration * 0.034 / 2;

        // Print the distance on the serial monitor
        Serial.print("Distance: ");
        Serial.print(distance);
        Serial.println(" cm");
        break;

      default:
        Serial.println("Invalid input, please enter 1, 2, 3, 4, or 5.");
        break;
    }
  }
}
