#include <Servo.h>

#define SERVO1_PIN 11
#define SERVO2_PIN 10
#define SERVO3_PIN 9
#define SERVO4_PIN 6
#define PIR_PIN 12
#define TRIG_PIN 3
#define ECHO_PIN 2

int pos = 0;

Servo servo_1;
Servo servo_2;
// Servo servo_3;
// Servo servo_4;

int ml_input = 0;

void setup() {
  servo_1.attach(SERVO1_PIN);
  servo_2.attach(SERVO2_PIN);
  // servo_3.attach(SERVO3_PIN);
  // servo_4.attach(SERVO4_PIN);
  // pinMode(PIR_PIN, INPUT);
  // scale.begin(A1, A0);
  Serial.begin(9600);
}

void loop() {
  // for (pos = 0; pos <= 180; pos += 1) {
  //   servo_1.write(pos);  // Tell servo to go to position in variable 'pos'
  //   delay(15);           // Wait for the servo to reach the position
  // }

  // // Sweep the servo from 180 to 0 degrees
  // for (pos = 180; pos >= 0; pos -= 1) {
  //   servo_1.write(pos);  // Tell servo to go to position in variable 'pos'
  //   delay(15);           // Wait for the servo to reach the position
  // }
  servo_1.write(0);
  servo_2.write(0);
  while (Serial.available() > 0) {
    // Read the incoming byte
    
    ml_input = Serial.parseInt();  // Read integer value from serial
    if (ml_input == 112) {
      servo_1.write(180);
      delay(1000);
      servo_1.write(0);
      // checkMotionAndReset(servo_1);
    } 
    else if (ml_input == 99) {
      servo_2.write(180);
      delay(1000);
      servo_2.write(0);
      // checkMotionAndReset(servo_2);
    }
  }

  // if (ml_input == 112) {
  //   servo_1.write(180);
  //   delay(1000);
  //   servo_1.write(0);
  //   // checkMotionAndReset(servo_1);
  // } else if (ml_input == 99) {
  //   servo_2.write(180);
  //   delay(1000);
  //   servo_2.write(0);
  //   // checkMotionAndReset(servo_2);
  // }
  // else if (ml_input == 109) {
  //   servo_3.write(180);
  //   checkMotionAndReset(servo_3);
  // }
  // else if (ml_input == 111) {
  //   servo_4.write(180);
  //   checkMotionAndReset(servo_4);
  // }
  // else {
  //   Serial.println("Invalid Error in ml.");
  // }
  // Serial.println("hi");
  // int cm = 0.0344/2 * readUltrasonicDistance(TRIG_PIN, ECHO_PIN);
  // Serial.print("Distance in cm: ");
  // Serial.println(cm);
  // if(cm < 5){
  //   Serial.println("dustbin full");
  // }
  // Serial.println(scale.get_units()/420);
  // delay(2000);
}

void checkMotionAndReset(Servo &servo) {
  while (digitalRead(PIR_PIN) == LOW) {
    Serial.println("waiting for motion.");
  }
  while (digitalRead(PIR_PIN) == HIGH) {
    Serial.println("motion detected.");
  }
  Serial.println("Motion Ended");
  servo.write(0);
}

long readUltrasonicDistance(int triggerPin, int echoPin) {
  pinMode(triggerPin, OUTPUT);  // Clear the trigger
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  // Sets the trigger pin to HIGH state for 10 microseconds
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  pinMode(echoPin, INPUT);
  // Reads the echo pin, and returns
  // the sound wave travel time in microseconds
  return pulseIn(echoPin, HIGH);
}
