import Function_Library as fl

arduino_port = 'COM7'

ser = fl.libARDUINO()

comm = ser.init(arduino_port, 9600)


while True:
    input_value = input('아두이노로 전송할 저항 값(0~255): ')

    comm.write(input_value.encode())

    if input_value == 'q':
        break