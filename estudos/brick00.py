#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep

ev3 = EV3Brick()

ev3.speaker.beep()

class Sumo:
    def _init_(self, velocidade, wheel_diameter, wheel_distance):
        self.velocidade = velocidade
        self.wheel_diameter = wheel_diameter
        self.wheel_lenght = wheel_diameter * 3.1415
        self.wheel_distance = wheel_distance
        self.r_motor = Motor(Port.A) # esses motores provavelmente não vão mudar de lugar
        self.l_motor = Motor(Port.B)
        self.r1_motor = Motor(Port.D) # esses motores provavelmente não vão mudar de lugar
        self.l1_motor = Motor(Port.C)
        self.ultra_sens1 = UltrasonicSensor(Port.S1) #sensor de cor na frente
        self.ultra_sens2 = UltrasonicSensor(Port.S2) #sensor de cor na frente 
     
    def walk(self, speed=300):
        self.r_motor.run(speed)
        self.l_motor.run(speed)
        self.r1_motor.run(-speed)
        self.l1_motor.run(-speed)

    def attack(self, speed=450): # ataque com mais velocidade
            self.r_motor.run(speed)
            self.l_motor.run(speed)
            self.r1_motor.run(-speed)
            self.l1_motor.run(-speed)

    def hold_motors(self):
        self.r_motor.hold()
        self.l_motor.hold()
        self.r1_motor.hold()
        self.l1_motor.hold()

    def brake_motors(self):
        self.r_motor.brake()
        self.l_motor.brake()
        self.r1_motor.brake()
        self.l1_motor.brake()

    def right(self, angle, speed):
        print("\n----------------DIREITA----------------")
        self.l_motor.reset_angle(0)
        self.r_motor.reset_angle(0)
        self.r1_motor.reset_angle(0)
        self.l1_motor.reset_angle(0)
        media_motor = 0
        graus_motor = angle * (self.wheel_distance / self.wheel_diameter)
    
        while media_motor < graus_motor:
            self.l_motor.run(speed)
            self.r_motor.run(-speed)
            self.r1_motor.run(speed)
            self.l1_motor.run(-speed)
            print(media_motor)
            media_motor = (self.l_motor.angle() - self.r_motor.angle()) / 2 # entender melhor o comportamento do media motor
        self.r_motor.hold()
        self.l_motor.hold()
        self.r1_motor.hold()
        self.l1_motor.hold()

    def left(self, angle, speed=100):
        print("\n----------------ESQUERDA----------------")
        self.l_motor.reset_angle(0)
        self.r_motor.reset_angle(0)
        self.r1_motor.reset_angle(0)
        self.l1_motor.reset_angle(0)
       
        media_motor = 0
        graus_motor = angle * (self.wheel_distance / self.wheel_diameter) 
        
        while media_motor < graus_motor: # para de girar até identificar que girou o ângulo ideal
            self.l_motor.run(-speed)
            self.r_motor.run(speed)
            self.r1_motor.run(-speed)
            self.l1_motor.run(speed)
            print(media_motor)
            media_motor = -1*((self.l_motor.angle()) - self.r_motor.angle()) / 2 # entender melhor o comportamento do media motor
        self.r_motor.hold()
        self.l_motor.hold()
        self.r1_motor.hold()
        self.l1_motor.hold()

robo_sumo = Sumo(100,4.5,11.8) 

def search(speed=200):
    angle=120
    #ponto inicial
    robo_sumo.right(angle, speed)
    robo_sumo.hold_motors()
    robo_sumo.left(2*angle, speed)
    robo_sumo.hold_motors()
    robo_sumo.right(95, speed) # fazer ele retornar do ponto inicial
    sleep(0.5) 
        
def main():
    ENEMY_DISTANCE = 100
    flag = 0
    
    while not flag:  # espera pelo botão central
        for button in ev3.buttons.pressed():
            print(button)
            if button == Button.CENTER:
                flag = 1

    distance = (robo_sumo.ultra_sens1.distance() + robo_sumo.ultra_sens2.distance()) / 2 # media dos dois sensores ultrassônicos
    while distance >= ENEMY_DISTANCE:
        search()
        sleep(3)
        distance = (robo_sumo.ultra_sens1.distance() + robo_sumo.ultra_sens2.distance()) / 2
        robo_sumo.walk()
        sleep(2)
    robo_sumo.attack()

main()