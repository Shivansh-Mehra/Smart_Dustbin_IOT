// #include <HX711_ADC.h>
// HX711_ADC LoadCell4(4, 5);

// void setup() {
//   // put your setup code here, to run once:
//   LoadCell4.begin();
//   LoadCell4.start(2000);
//   LoadCell4.setCalFactor(390);

//   Serial.begin(9600);
//   Serial.println("Setup Ended");
// }

// void loop() {
//   // put your main code here, to run repeatedly:
//   LoadCell4.update();  // retrieves data from the load cell
//   float totalWeight = 0;
//   const int numReadings = 30;  // number of readings to average
//   for (int i = 0; i < numReadings; i++) {
//     LoadCell4.update();  // get the latest reading
//     LoadCell4.getData();
//     if (i > 20) {
//       totalWeight += LoadCell4.getData();  // add the reading
//     }
//     delay(100);  // short delay to stabilize between readings
//   }
//   float weight = totalWeight / 9;  // calculate average
//   Serial.print("Weight[g]:");
//   Serial.println(weight);
// }

#include <HX711_ADC.h>

HX711_ADC LoadCell4(A0, A1);  // HX711 DT and SCK pins

void setup() {
  Serial.begin(9600);
  LoadCell4.begin();
  LoadCell4.start(2000);  // Allow some time to stabilize
  LoadCell4.setCalFactor(390);  // Calibration factor (adjust based on your setup)
  Serial.println("Setup Complete");
}

void loop() {
  LoadCell4.update();  // Update the load cell data
  float totalWeight = 0;
  const int numReadings = 10;  // Number of readings to average

  // Collect multiple readings to stabilize the result
  for (int i = 0; i < numReadings; i++) {
    LoadCell4.update();
    float weightReading = LoadCell4.getData();
    
    // Print each reading for debugging
    Serial.print("Reading ");
    Serial.print(i + 1);
    Serial.print(": ");
    Serial.println(weightReading);

    totalWeight += weightReading;
    delay(100);  // Short delay between readings
  }

  // Calculate average weight
  float averageWeight = totalWeight / numReadings;
  Serial.print("Average Weight[g]: ");
  Serial.println(averageWeight);

  delay(2000);  // Wait before the next reading
}

