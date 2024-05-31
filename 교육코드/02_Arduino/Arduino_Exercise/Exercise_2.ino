#include <Car_Library.h>

int analogPin = A5;   // 가변저항 Output Pin

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);       // 시리얼 통신 시작, 통신 속도 설정
  pinMode(LED_BUILTIN, OUTPUT);     // LED 핀 모드 설정
}

void loop() {
  // put your main code here, to run repeatedly:
  int val;      // 저항값 저장할 변수 선언

  // 가변저항의 저항값을 읽어오는 함수 실행
  val = potentiometer_Read(analogPin);

  // Serial 모니터로 출력
  Serial.println(val);

  // 가변 저항 값을 LED로 보내 출력
  analogWrite(LED_BUILTIN, val);
}
