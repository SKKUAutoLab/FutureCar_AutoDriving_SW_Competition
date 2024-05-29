#include <Car_Library.h>

int motorA1 = 3;    // 모터 드라이버 IN1
int motorA2 = 4;    // 모터 드라이버 IN2


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);       // 시리얼 통신 시작, 통신 속도 설정
  pinMode(motorA1, OUTPUT);
  pinMode(motorA2, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  // Forward
  Serial.println("Motor Forward");
  motor_forward(motorA1, motorA2, 75);
  delay(3000);

  // Backward
  Serial.println("Motor Backward");
  motor_backward(motorA1, motorA2, 150);
  delay(3000);

  // Hold
  Serial.println("Motor Hold");
  motor_hold(motorA1, motorA2);
  delay(3000);
}
