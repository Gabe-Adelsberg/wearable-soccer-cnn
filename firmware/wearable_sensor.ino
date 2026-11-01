#include "DFRobot_BMI160.h"
#include <SPI.h>
#include <SD.h>

const int CS_PIN = 10;
const int8_t I2C_ADDRESS = 0x69;
const char *DATA_FILE = "data.txt";

DFRobot_BMI160 bmi160;
File dataFile;

void setup() {
  Serial.begin(115200);
  delay(100);

  if (bmi160.softReset() != BMI160_OK) {
    Serial.println("BMI160 reset failed");
    while (true) {}
  }

  if (bmi160.I2cInit(I2C_ADDRESS) != BMI160_OK) {
    Serial.println("BMI160 initialization failed");
    while (true) {}
  }

  initializeSD();

  if (SD.exists(DATA_FILE)) {
    writeData("\n");
  }

  writeHeader();
}

void loop() {
  int16_t accelGyro[6] = {0};
  const int result = bmi160.getAccelGyroData(accelGyro);

  if (result != 0) {
    Serial.println("BMI160 read error");
    return;
  }

  // BMI160 library order used in the original project:
  // first three values = gyroscope, last three = acceleration.
  for (int i = 0; i < 6; ++i) {
    float value;

    if (i < 3) {
      value = accelGyro[i] * 3.14159265f / 180.0f;
    } else {
      value = accelGyro[i] / 16384.0f;
    }

    Serial.print(value);
    Serial.print(i == 5 ? '\n' : '\t');

    writeData(String(value) + (i == 5 ? "\n" : ","));
  }
}

void initializeSD() {
  Serial.print("Initializing SD card... ");

  if (!SD.begin(CS_PIN)) {
    Serial.println("failed");
    while (true) {}
  }

  Serial.println("success");
}

void writeHeader() {
  dataFile = SD.open(DATA_FILE, FILE_WRITE);

  if (!dataFile) {
    Serial.println("Error opening data file");
    return;
  }

  dataFile.println("X_Gyro,Y_Gyro,Z_Gyro,X_Acc,Y_Acc,Z_Acc");
  dataFile.close();
}

void writeData(const String &value) {
  dataFile = SD.open(DATA_FILE, FILE_WRITE);

  if (!dataFile) {
    Serial.println("Error opening data file");
    return;
  }

  dataFile.print(value);
  dataFile.close();
}
