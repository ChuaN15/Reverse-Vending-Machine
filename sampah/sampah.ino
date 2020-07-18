#include <Servo.h>

#define servoPin 3

Servo servo;

int echoPin[] = { , , };
int trigPin[] = { , , };




void setup() {
  Serial.begin(9600);

  servo.attach(servoPin);
  
  for (int a = 0; a<3; a++){
    pinMode(echoPin[a], OUTPUT);
    pinMode(trigPin[a], INPUT);
  }

}

void loop() {
  // put your main code here, to run repeatedly:

}
