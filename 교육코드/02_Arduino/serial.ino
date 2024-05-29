#include <Car_Library.h>

int val;           // 수신된 값 저장할 변수

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);       // 시리얼 통신 시작, 통신 속도 설정
  pinMode(LED_BUILTIN, OUTPUT);     // LED 핀 모드 설정
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()) {
    val = Serial.parseInt();

    if(val >= 0) {
      analogWrite(LED_BUILTIN, val);
    }
  }
}