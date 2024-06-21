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

# achei num repositório e quis testar aqui
ev3.speaker.set_volume(volume=100, which="_all_")
ev3.speaker.set_speech_options(language="pt-pt", voice="whisperf")
ev3.speaker.say("RO BO FOR GE")
ev3.speaker.beep(frequency=1000, duration=100)

class Sumo:
    def __init__(self, velocidade, wheel_diameter, wheel_distance):
        self.velocidade = velocidade
        self.wheel_lenght = wheel_diameter * 3.1415
        self.wheel_distance = wheel_distance
        self.r_motor = Motor(Port.B) # esses motores provavelmente não vão mudar de lugar
        self.l_motor = Motor(Port.C)
        self.color_front = ColorSensor(Port.S1) #sensor de cor na frente 
        self. ultra_front = UltrasonicSensor(Port.S2) #sensor ultrassonico na frente  

    def walk(self, speed=100):
        self.r_motor.run(speed)
        self.l_motor.run(speed)

    def attack(self, speed=250): # ataque com mais velocidade
        while self.color_front.color() != color.WHITE:
            self.r_motor.run(speed)
            self.l_motor.run(speed)

    def hold_motors(self):
        self.r_motor.hold()
        self.l_motor.hold()
    
    def brake_motors(self):
        self.r_motor.brake()
        self.l_motor.brake()

    def right(self, angle, speed):
        self.l_motor.reset_angle(0)
        self.r_motor.reset_angle(0)
        media_motor = 0
        graus_motor = angle * (self.wheel_distance / self.wheel.diameter)
        while media_motor < graus_motor:
            self.l_motor.run(speed)
            self.r_motor.run(-speed)
            media_motor = (self.l_motor.angle() - self.r_motor.angle()) / 2
        print(f"\nO motor girou para direita {media_motor} graus")
        self.l_motor.hold()
        self.r_motor.hold()

    def left(self, angle, speed=100):
        self.l_motor.reset_angle(0)
        self.r_motor.reset_angle(0)
        media_motor = 0
        graus_motor = angle * (self.wheel_distance / self.wheel.diameter)
        while media_motor < graus_motor: # para de girar até identificar que girou o ângulo ideal
            self.l_motor.run(-speed)
            self.r_motor.run(speed)
            media_motor = (self.l_motor.angle() - self.r_motor.angle()) / 2
        print(f"\nO motor girou para a esqueerda {media_motor} graus")
        self.l_motor.hold()
        self.r_motor.hold()

robo_sumo = Sumo(100,5.5,11.5) # meu objeto <3 

def search (speed=100):
    while True:
        robo_sumo.right(120)
        robo_sumo.left(120)
        robo_sumo.right(30)
        robo_sumo.walk(200)
        sleep(4)
        robo_sumo.left(180)
        robo_sumo.right(120)
        robo_sumo.left(120)
        
def main():
    
    ENEMY_DISTANCE = 800 
    flag = 0
    
    while not flag: # para garantir que o botão vai ser apertado
        for button in ev3.buttons.pressed():
            print(button)
            if button == Button.CENTER:
                flag = 1
    sleep(5)
    
    while True:
        robo_sumo.walk()
        robo_sumo.hold_motors()
        robo_sumo.brake_motors()
        robo_sumo.attack()
        robo_sumo.right(90)
        robo_sumo.left(90)
        sleep(5)
        distance = robo_sumo.ultra_front.distance()
        
        if distance <= ENEMY_DISTANCE:
            robo_sumo.attack()
        
        else:
            robo_sumo.search()
main()
