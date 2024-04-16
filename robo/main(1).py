#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from time import sleep

ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
l_color_sensor = ColorSensor(Port.S2)
r_color_sensor = ColorSensor(Port.S3)

# futuramente criar uma calibração de cores usando árvore de decisão
white = (70,70,70)
red = (63,50,20)
black = (5,5,5)
green = (10,17,10)
yellow = (58,39,26)

DIST_ENTRE_RODAS = 10.0
DIAMETRO_RODA = 5.5


def go_straight(velocity):
    left_motor.run(velocity)
    right_motor.run(velocity)


def turn_right(angle):
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    media_motor = 0
    graus_motor = angle * (DIST_ENTRE_RODAS / DIAMETRO_RODA)
    while media_motor < graus_motor:
        left_motor.run(100)
        right_motor.run(-100)
        media_motor = (left_motor.angle() - right_motor.angle()) / 2
        print(media_motor)
    left_motor.hold()
    right_motor.hold()


def turn_left(angle):
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    media_motor = 0
    graus_motor = angle * (DIST_ENTRE_RODAS / DIAMETRO_RODA)
    while media_motor < graus_motor:
        left_motor.run(-100)
        right_motor.run(100)
        media_motor = (left_motor.angle() - right_motor.angle()) / 2
    left_motor.hold()
    right_motor.hold()


def realign(motorB, motorC):
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)

    r,g,b = l_color_sensor.rgb()
    while r_color_sensor() != : # enquanto for diferente de branco
        motorB.run(speed=-70)
        dB = (motorB.angle()*DIAMETRO_RODA*3.14)/360
    dC = 0
    while dC <= dB:
        motorC.run(speed=-70)
        dC = (motorB.angle()*DIAMETRO_RODA*3.14)/360
    motorB.hold()
    motorC.hold()


def brake():
    left_motor.stop()
    right_motor.stop()

"""def verify_white(sensor):
    r,g,b = sensor.rgb() 
    if r >= white[0] and g <= white[1] and b <= white[2]:
        return True
    return False

def verify_red(sensor):
    r,g,b = sensor.rgb() 
    if r >= red[0] and g <= red[1] and b <= red[2]:
        return True
    return False

def verify_black(sensor):
    r,g,b = sensor.rgb() 
    if r <= black[0] and g <= black[1] and b <= black[2]:
        return True
    return False

def verify_green(sensor):
    r,g,b = sensor.rgb() 
    if r <= green[0] and g >= green[1] and b <= green[2]:
        return True
    return False

def verify_yellow(sensor):
    r,g,b = sensor.rgb() 
    if r >= yellow[0] and g >= yellow[1] and b <= yellow[2]:
        return True
    return False
"""

def main():
    # configurações de parâmetros iniciais
    velocity = 100
    back = 10 # quantos centimetros pra recuar
    distance = 20 # distancia para percorrer no corredor que vai diferenciar os 2 casos
    
    while True:
        
        go_straight(velocity)
        
        if verify_black(l_color_sensor) and verify_black(r_color_sensor): # se o sensor identificar o preto ele para e vira para esquerda
            brake() 
            realign(left_motor, right_motor) # realinhar as rodas
            center = 0
            
            while center < back: # recuar para o centro do corredor
                left_motor.run(speed=-70)
                right_motor(speed=-70)
                center += (left_motor.angle()*DIAMETRO_RODA*3.1415)/360 # acumula o valor da distancia
            
            turn_left(90)
            
            go_straight(velocity) 
            
            left_motor.reset_angle(0)
            right_motor.reset_angle(0)
            
            cmB = (left_motor.angle()*DIAMETRO_RODA*3.14)/360 # distancia para verificar
            
            while not verify_black(l_color_sensor) and not verify_black(r_color_sensor) or cmB < distance:  
                go_straight(velocity)
            brake()

            if verify_black(l_color_sensor) and verify_black(r_color_sensor):
                brake()
                turn_right(180)

if __name__ == '__main__':
    main()