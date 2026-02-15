int energyScore = 0;

int throttleInput = 255;
int throttleOutput = 0;
float k = 1.0;

const int pwmPin = 25;
const int pwmChannel = 0;
const int pwmFreq = 5000;
const int pwmResolution = 8;

void setup() {
  Serial.begin(9600);

  ledcSetup(pwmChannel, pwmFreq, pwmResolution);
  ledcAttachPin(pwmPin, pwmChannel);
}

void loop() {

  if (Serial.available() > 0) {
    energyScore = Serial.parseInt();
  }

  if (energyScore >= 80) k = 1.0;
  else if (energyScore >= 60) k = 0.85;
  else if (energyScore >= 40) k = 0.7;
  else k = 0.5;

  throttleOutput = throttleInput * k;

  ledcWrite(pwmChannel, throttleOutput);

  delay(300);
}