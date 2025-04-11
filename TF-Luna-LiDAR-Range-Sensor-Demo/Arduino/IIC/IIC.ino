#include <Wire.h>

byte deviceAddress = 0x10;  // The address of the TF-Luna device is 0x10

void setup() {
  Wire.begin();             // The I2C bus communication starts
  Serial.begin(115200);       // Example Set the baud rate of the serial port to 115200
}

void loop() {
  Wire.beginTransmission(deviceAddress);  // The I2C data transmission starts
  Wire.write(0x00);                       // Send command
  Wire.endTransmission();                 // The I2C data transfer is complete

  Wire.requestFrom((uint8_t)deviceAddress, (uint8_t)7);     // Read 7 bytes of data 

  if (Wire.available() == 7) {            // 7 bytes of data are available
    byte data[7];
    for (int i = 0; i < 7; i++) {
      data[i] = Wire.read();              // Read data into an array
    }

    unsigned int distance = (data[1] << 8) | data[0];                   // DistanceValue
    unsigned int signalStrength = (data[3] << 8) | data[2];             // signal strength

    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.print(" cm  \n");

    Serial.print("Signal Strength: ");
    Serial.print(signalStrength);
    Serial.print("\n");
  }

  delay(10);               
}