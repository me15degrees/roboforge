#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep


WHEEL_DIAMETER = 5.5
WHEEL_DISTANCE = 11.5

ev3 = EV3Brick()
stopwatch = StopWatch()
ev3.speaker.beep() #para mostrar que está funcionando o código

motor_a = Motor(Port.A)
motor_b = Motor(Port.B) #motores b, c costumam ser para movimentação do robô
motor_c = Motor(Port.C)
motor_d = Motor(Port.D)
color_front = ColorSensor(Port.S1) #sensor de cor na frente 
ultra_front = UltrasonicSensor(Port.S2) #sensor ultrassonico na frente  


def walk(speed = 100):
    motor_a.dc(speed)
    motor_d.dc(-speed)
    motor_b.dc(speed)
    motor_c.dc(-speed)


def hold_motors():
    motor_a.hold()
    motor_d.hold()
    motor_b.hold()
    motor_c.hold()
   
def brake_motors():
    motor_a.brake()
    motor_d.brake()
    motor_b.brake()
    motor_c.brake()


def scan(speed = 35):
    motor_a.dc(-speed)
    motor_d.dc(-speed)
    motor_b.dc(speed)
    motor_c.dc(speed)
    

def main():
    robot_distance = 500
    flag = 0
    stopwatch.reset()
    while not flag:
        for button in ev3.buttons.pressed():
            print(button)
            if button == Button.CENTER:
                flag = 1
    sleep(5)
    while True:
        distance = ultra_front.distance()
        if distance < robot_distance:
            while(color_front.color() != Color.WHITE and distance < robot_distance):
                print(ultra_front.distance())
                previous_distance = distance
                if distance != 2550 and ultra_front.distance() < 10*previous_distance: 
                    distance = ultra_front.distance()
                walk()
            if(color_front.color() == Color.WHITE):
                brake_motors()
                walk(speed = -80)
                sleep(1.5)
            hold_motors()
        else:
            while(distance > robot_distance):
                distance = ultra_front.distance()
                if stopwatch.time() > 2000:
                    scan(-35)
                    if stopwatch.time() > 4000:
                        stopwatch.reset()
                else:
                    scan()
            hold_motors()

main()
