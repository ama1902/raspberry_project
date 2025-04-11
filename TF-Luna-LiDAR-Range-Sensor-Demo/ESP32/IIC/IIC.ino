#include <Wire.h> 
#define SLAVE_ADDRESS 0x10 // I2C Indicates the address of the secondary device
#define COMMAND 0x00 // order
#define DATA_LENGTH 9 // data length

unsigned char buf1[] = {0x5A,0x05,0x00,0x01,0x60};
void setup() {
  Wire.begin(17,16); // Initializes the Wire library
  Serial.begin(115200); // Initializing serial port

}

void loop() {
  Wire.beginTransmission(SLAVE_ADDRESS);  // The I2C data transmission starts
  Wire.write(buf1,5);                       // send instructions
  Wire.endTransmission();                 // The I2C data transfer is complete
  Wire.requestFrom(SLAVE_ADDRESS, DATA_LENGTH); // Request data from an I2C device
  uint8_t data[DATA_LENGTH] = {0}; 
  uint16_t distance = 0, strength = 0; // Data variable
  int16_t temperature = 0;
  int checksum = 0;
  int index = 0; 
  while (Wire.available() > 0 && index < DATA_LENGTH) {
    data[index++] = Wire.read(); // Read data into an array
  }
  if (index == DATA_LENGTH) {
    distance = data[2] + data[3] * 256; //  DistanceValue
    strength = data[4] + data[5] * 256; // signal strength
    temperature = data[6] + data[7] * 256; // Chip temperature
      Serial.print("Distance: ");
      Serial.print(distance);
      Serial.print(" cm, strength: ");
      Serial.print(strength);
      Serial.print(", temperature: ");
      Serial.println(temperature / 8.0 - 256.0);
    
  }
  delay(10); 
}