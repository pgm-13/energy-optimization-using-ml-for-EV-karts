#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>

MCUFRIEND_kbv tft;

int energyScore = 0;
int driverScore = 0;

void setup() {
  Serial.begin(9600);

  uint16_t id = tft.readID();
  tft.begin(id);
  tft.setRotation(1);

  tft.fillScreen(0x0000);
  tft.setTextColor(0xFFFF);
  tft.setTextSize(2);
  tft.setCursor(40, 200);
  tft.print("Waiting for ML data...");
}

void loop() {

  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int commaIndex = data.indexOf(',');

    if (commaIndex > 0) {
      energyScore = data.substring(0, commaIndex).toInt();
      driverScore = data.substring(commaIndex + 1).toInt();
      drawScreen();
    }
  }
}

void drawScreen() {

  tft.fillScreen(0x0000);

  tft.setTextColor(0xFFFF);
  tft.setTextSize(3);
  tft.setCursor(40, 20);
  tft.print("PREVIOUS LAP SCORES");

  tft.setTextSize(2);
  tft.setCursor(40, 70);
  tft.print("Energy Score:");

  tft.setTextSize(4);
  tft.setCursor(80, 100);
  tft.print(energyScore);

  tft.setTextSize(2);
  tft.setCursor(40, 160);
  tft.print("Driver Score:");

  tft.setTextSize(4);
  tft.setCursor(80, 190);
  tft.print(driverScore);

  tft.setTextSize(2);
  tft.setCursor(40, 250);

  if (energyScore >= 80) {
    tft.setTextColor(0x07E0);
    tft.print("Full Performance Mode");
  }
  else if (energyScore >= 60) {
    tft.setTextColor(0xFFE0);
    tft.print("Mild Restriction");
  }
  else if (energyScore >= 40) {
    tft.setTextColor(0xFD20);
    tft.print("Energy Protection Mode");
  }
  else {
    tft.setTextColor(0xF800);
    tft.print("Critical Energy Mode");
  }

  tft.setTextColor(0xFFFF);
  tft.setCursor(40, 300);

  if (driverScore >= 90) {
    tft.print("Push Hard on Straights");
  }
  else if (driverScore >= 75) {
    tft.print("Increase Exit Speed");
  }
  else if (driverScore >= 50) {
    tft.print("Improve Corner Flow");
  }
  else if (driverScore >= 30) {
    tft.print("Reduce Steering Corrections");
  }
  else {
    tft.print("Try smoother Inputs & Control");
  }
}