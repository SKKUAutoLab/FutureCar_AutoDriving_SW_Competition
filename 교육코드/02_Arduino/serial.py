import Function_Library as fl

arduino_port = 'COM7'

ser = fl.arduino_init(arduino_port)

while True:
    input_value = input('아두이노로 전송할 저항 값(0~255): ')

    ser.write(input_value.encode())

    if input_value == 'q':
        break