#include <Servo.h>
#include <HX711_ADC.h>

// Load Cell pins
HX711_ADC LoadCell1(A0, A1);
HX711_ADC LoadCell2(A2, A3);
HX711_ADC LoadCell3(A4, A5);
HX711_ADC LoadCell4(4, 5);

// Servo pins
#define SERVO1_PIN 11
#define SERVO2_PIN 10
#define SERVO3_PIN 9
#define SERVO4_PIN 6
#define PIR_PIN 12

// Ultrasonic Sensor pins
#define TRIG_PIN 3
#define ECHO_PIN 2

Servo servo_1;
Servo servo_2;
Servo servo_3;
Servo servo_4;

int ml_input = 0;
long duration;
int distance;

void setup() {
  // Attach servos
  servo_1.attach(SERVO1_PIN);
  servo_2.attach(SERVO2_PIN);
  servo_3.attach(SERVO3_PIN);
  servo_4.attach(SERVO4_PIN);
  
  // Set servos to initial position
  servo_1.write(0);
  servo_2.write(0);
  servo_3.write(0);
  servo_4.write(0);
  
  // Setup load cells
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

  // Set up ultrasonic sensor pins
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  Serial.begin(9600);
  Serial.println("Setup Ended");
}

void loop() {
  if (ml_input == 0) {
    while (Serial.available() == 0) {}
    ml_input = Serial.parseInt();
  }

  while (Serial.available() == 0) {}

  String inputString = Serial.readStringUntil('\n');
  inputString.trim();

  if (inputString == "s") {
    handleServoAction();
  } else if (inputString == "w") {
    handleWeightAction();
  } else if (inputString == "d") {
    // Ultrasonic distance measurement
    distance = readUltrasonicDistance(TRIG_PIN, ECHO_PIN);
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");
  } else {
    Serial.println("Invalid input.");
  }
}

// Function to control servos based on ml_input
void handleServoAction() {
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
    Serial.println("Invalid ml_input for servo.");
  }
}

// Function to read weights from the load cells
void handleWeightAction() {
  if (ml_input == 112) {
    readWeight(LoadCell1);
  } else if (ml_input == 99) {
    readWeight(LoadCell2);
  } else if (ml_input == 109) {
    readWeight(LoadCell3);
  } else if (ml_input == 103) {
    readWeight(LoadCell4);
  } else {
    Serial.println("Invalid ml_input for weight.");
  }
}

// Function to read weight from the load cell and average the values
void readWeight(HX711_ADC& loadCell) {
  loadCell.update();
  float totalWeight = 0;
  const int numReadings = 30;
  
  for (int i = 0; i < numReadings; i++) {
    loadCell.update();
    if (i > 20) {
      totalWeight += loadCell.getData();
    }
    delay(100);
  }
  
  float weight = totalWeight / 9;
  Serial.print("Weight[g]: ");
  Serial.println(weight);
}

// Function to read the distance from the ultrasonic sensor
long readUltrasonicDistance(int triggerPin, int echoPin) {
  // Send a pulse to trigger the ultrasonic sensor
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);

  // Measure the time it takes for the pulse to bounce back
  long duration = pulseIn(echoPin, HIGH);

  // Calculate the distance based on the time of travel
  long distance = duration * 0.034 / 2; // distance in cm
  return distance;
}
