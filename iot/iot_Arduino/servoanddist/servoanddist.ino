#include <Servo.h>
#include <HX711_ADC.h>

HX711_ADC LoadCell1(A0, A1);
HX711_ADC LoadCell2(A2, A3);
HX711_ADC LoadCell3(A4, A5);
HX711_ADC LoadCell4(4, 5);


#define SERVO1_PIN 11
#define SERVO2_PIN 10
#define SERVO3_PIN 9
#define SERVO4_PIN 6
#define PIR_PIN 12
#define TRIG_PIN 3
#define ECHO_PIN 2

Servo servo_1;
Servo servo_2;
Servo servo_3;
Servo servo_4;

int ml_input = 0;

void setup() {
  servo_1.attach(SERVO1_PIN);
  servo_2.attach(SERVO2_PIN);
  servo_3.attach(SERVO3_PIN);
  servo_4.attach(SERVO4_PIN);
  servo_1.write(0);
  servo_2.write(0);
  servo_3.write(0);
  servo_4.write(0);
  LoadCell1.begin();
  LoadCell1.start(2000);
  LoadCell1.setCalFactor(390);
  LoadCell2.begin();
  LoadCell2.start(2000);
  LoadCell2.setCalFactor(390);
  LoadCell3.begin();
  LoadCell3.start(2000);
  LoadCell3.setCalFactor(390);
  LoadCell4.begin();
  LoadCell4.start(2000);
  LoadCell4.setCalFactor(390);
  // pinMode(PIR_PIN, INPUT);
  // LoadCell1.begin();
  // LoadCell1.start(2000);
  // LoadCell1.setCalFactor(390);
  Serial.begin(9600);
  Serial.println("Setup Ended");
}

void loop() {
  if (ml_input == 0) {
    while (Serial.available() == 0) {
    }
    ml_input = Serial.parseInt();
  }
  while (Serial.available() == 0) {
  }
  String inputString = Serial.readStringUntil('\n');
  inputString.trim();
  if (inputString == "s") {
    if (ml_input == 112) {
      servo_1.write(180);
      delay(2000);
      servo_1.write(0);
    } else if (ml_input == 99) {
      servo_2.write(90);
      delay(2000);
      servo_2.write(0);
    } else if (ml_input == 109) {
      servo_3.write(120);
      delay(2000);
      servo_3.write(0);
    } else if (ml_input == 103) {
      servo_4.write(120);
      delay(2000);
      servo_4.write(0);
    } else {
      Serial.println("Invalid Error in ml from servo.");
    }
  } else if (inputString == "w") {
    if (ml_input == 112) {
      // LoadCell1.begin();
      // LoadCell1.start(2000);
      // LoadCell1.setCalFactor(390);
      LoadCell1.update();  // retrieves data from the load cell
      float totalWeight = 0;
      const int numReadings = 30;  // number of readings to average
      for (int i = 0; i < numReadings; i++) {
        LoadCell1.update();  // get the latest reading
        LoadCell1.getData();
        if (i > 20) {
          totalWeight += LoadCell1.getData();  // add the reading
        }
        delay(100);  // short delay to stabilize between readings
      }
      float weight = totalWeight / 9;  // calculate average
      Serial.print("Weight[g]:");
      Serial.println(weight);
    } else if (ml_input == 99) {
      // LoadCell2.begin();
      // LoadCell2.start(2000);
      // LoadCell2.setCalFactor(390);
      LoadCell2.update();  // retrieves data from the load cell
      float totalWeight = 0;
      const int numReadings = 30;  // number of readings to average
      for (int i = 0; i < numReadings; i++) {
        LoadCell2.update();  // get the latest reading
        LoadCell2.getData();
        if (i > 20) {
          totalWeight += LoadCell2.getData();  // add the reading
        }
        delay(100);  // short delay to stabilize between readings
      }
      float weight = totalWeight / 9;  // calculate average
      Serial.print("Weight[g]:");
      Serial.println(weight);
    } else if (ml_input == 109) {
      // LoadCell3.begin();
      // LoadCell3.start(2000);
      // LoadCell3.setCalFactor(390);
      LoadCell3.update();  // retrieves data from the load cell
      float totalWeight = 0;
      const int numReadings = 30;  // number of readings to average
      for (int i = 0; i < numReadings; i++) {
        LoadCell3.update();  // get the latest reading
        LoadCell3.getData();
        if (i > 20) {
          totalWeight += LoadCell3.getData();  // add the reading
        }
        delay(100);  // short delay to stabilize between readings
      }
      float weight = totalWeight / 9;  // calculate average
      Serial.print("Weight[g]:");
      Serial.println(weight);
    } else if (ml_input == 103) {
      // LoadCell4.begin();
      // LoadCell4.start(2000);
      // LoadCell4.setCalFactor(390);
      LoadCell4.update();  // retrieves data from the load cell
      float totalWeight = 0;
      const int numReadings = 30;  // number of readings to average
      for (int i = 0; i < numReadings; i++) {
        LoadCell4.update();  // get the latest reading
        LoadCell4.getData();
        if (i > 20) {
          totalWeight += LoadCell4.getData();  // add the reading
        }
        delay(100);  // short delay to stabilize between readings
      }
      float weight = totalWeight / 9;  // calculate average
      Serial.print("Weight[g]:");
      Serial.println(weight);
    } else {
      Serial.println("Invalid Error in ml from weight.");
    }
  } else if (inputString == "d") {
    // Action for 'd'
    digitalWrite(TRIG_PIN , LOW);  // Clear the trigger pin
    delayMicroseconds(2);

    // Send a 10us HIGH pulse to the trigger pin to start measurement
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    // Read the echo pin and calculate the time it takes for the echo to return
    int duration = pulseIn(ECHO_PIN, HIGH);

    // Calculate the distance in centimeters
    int distance = duration * 0.034 / 2;

    // Print the distance on the serial monitor
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");
  } else {
    Serial.println("error");
  }
}


void checkMotionAndReset(Servo &servo) {
  digitalWrite(LED_BUILTIN, HIGH);
  while (digitalRead(PIR_PIN) == LOW) {
    Serial.println("waiting for motion.");
  }
  while (digitalRead(PIR_PIN) == HIGH) {
    Serial.println("motion detected");
  }
  digitalWrite(LED_BUILTIN, LOW);
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
