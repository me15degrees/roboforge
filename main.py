from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, Port
from pybricks.parameters import Color, Stop
from time import sleep

ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
color_sensor = ColorSensor(Port.S1)

def go_straight(velocity):
    left_motor.run(velocity)
    right_motor.run(velocity)

def turn_right(velocity):
    left_motor.run(velocity)
    right_motor.run(0)

def turn_left(velocity):
    left_motor.run(0)
    right_motor.run(velocity)

def brake():
    left_motor.stop()
    right_motor.stop()

def main():
    # configurações de parâmetros iniciais
    velocity = 90
    black = (5, 5, 5)
    distance_parameter = 20
    wheels_distance = 50 #fazer a logica dele usar isso para realmente girar 90 graus

    while True:
        go_straight(velocity)
        if color_sensor.rgb() <= black: # se o sensor identificar o preto ele para e vira para esquerda
            brake()
            turn_left(velocity)
            sleep(1) 
            distance_traveled = 0 
            go_straight(velocity=70) # anda reto mais devagar para não ter perigo de invadir o vermelho
            if color_sensor.rgb() <= black:
                brake()
                if distance_traveled < distance_parameter:  # se a distância percorrida for menor que 20 cm significa que deve virar para o outro lado
                    turn_right(velocity)     
                    sleep(1)                
                    go_straight(velocity=70)   
            
        go_straight(velocity)       # se não detectar preto, siga em frente

        sleep(2)  # aguarde um pouco antes de verificar novamente

if __name__ == '__main__':
    main()
