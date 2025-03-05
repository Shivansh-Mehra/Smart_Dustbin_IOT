const int trigPin = 3;   // Pin connected to the Trigger pin of the ultrasonic sensor
const int echoPin = 2;  // Pin connected to the Echo pin of the ultrasonic sensor
long duration;           // Variable for the duration of the sound wave travel
int distance;            // Variable for the calculated distance

void setup() {
  pinMode(trigPin, OUTPUT);  // Set the Trigger pin as output
  pinMode(echoPin, INPUT);   // Set the Echo pin as input
  Serial.begin(9600);        // Initialize serial communication at 9600 baud rate
}

void loop() {
  // Clear the trigger pin
  digitalWrite(trigPin, LOW);
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

  delay(1000);  // Wait for a second before the next measurement
}
