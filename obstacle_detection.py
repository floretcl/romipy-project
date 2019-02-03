#!/usr/bin/python3
# -*- coding:Utf-8 -*-

import RPi.GPIO as GPIO

from random import choice
from time import time, sleep

from engines import *

#________________PINS_______________________#

FAULT_DRV8833 = 7
DONT_SLEEP_DRV8833 = 8

MOTOR1_BACKWARD = 24
MOTOR1_FORWARD = 25
MOTOR2_BACKWARD = 22
MOTOR2_FORWARD = 23

SENSOR_LEFT = 12
SENSOR_RIGHT = 13

TRIG = 17
ECHO = 27

#______________INPUT/OUPUT__________________#

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(FAULT_DRV8833, GPIO.IN)
GPIO.setup(DONT_SLEEP_DRV8833, GPIO.OUT, initial=0)

GPIO.setup(MOTOR1_BACKWARD,GPIO.OUT)
GPIO.setup(MOTOR1_FORWARD,GPIO.OUT)
GPIO.setup(MOTOR2_BACKWARD,GPIO.OUT)
GPIO.setup(MOTOR2_FORWARD,GPIO.OUT)

GPIO.setup(TRIG, GPIO.OUT, initial=0)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(SENSOR_LEFT, GPIO.IN)
GPIO.setup(SENSOR_RIGHT, GPIO.IN)

#_______________PWM________________________#

pwm_motor1_forward = GPIO.PWM(MOTOR1_FORWARD, 50)
pwm_motor2_forward = GPIO.PWM(MOTOR2_FORWARD, 50)
pwm_motor1_backward = GPIO.PWM(MOTOR1_BACKWARD, 50)
pwm_motor2_backward = GPIO.PWM(MOTOR2_BACKWARD, 50)
pwm_motor1_forward.start(0)
pwm_motor1_backward.start(0)
pwm_motor2_forward.start(0)
pwm_motor2_backward.start(0)

#________________DEF_______________________#

def get_range():
    GPIO.output(TRIG, 0)
    sleep(0.1)
    GPIO.output(TRIG, 1)
    sleep(0.000010)
    GPIO.output(TRIG, 0)
    while GPIO.input(ECHO) == 0:
        pass
    start_time = time()
    while GPIO.input(ECHO) == 1:
        pass
    stop_time = time()
    record_time = stop_time - start_time
    distance = 17000 * record_time
    return distance



#________________TESTS_______________________#

def test_obstacle_detection(nb_measures):
    """TEST OBSTACLE DETECTION SENSORS DEMO"""

    GPIO.output(DONT_SLEEP_DRV8833, 1) # Activation de la puce DRV8833 pour les moteurs

    if not GPIO.input(FAULT_DRV8833): # Si défaut, le dire et s'arreter là
        print("ERROR FAULT_DRV8833")
    elif nb_measures <= 0 and not nb_measures.is_integer(): # Si problème de paramètre, le dire et s'arreter là
        print("ERROR PARAM")
    else: # Exécution du test

        while nb_measures >= 1: # Tant qu'il y a encore des mesures à faire
            
            not_obstacle_left = GPIO.input(SENSOR_LEFT)
            not_obstacle_right = GPIO.input(SENSOR_RIGHT)

            if not not_obstacle_left and not not_obstacle_right:
                #manoeuvre esquive
                print("manoeuvre esquive obstacle de tout coté")
                sleep(1)
            elif not not_obstacle_left and not_obstacle_right:
                #manoeuvre esquive
                print("manoeuvre esquive obstacle à gauche")
                sleep(1)
            elif not_obstacle_left and not not_obstacle_right:
                #manoeuvre esquive
                print("manoeuvre esquive obstacle à droite")
                sleep(1)
            else:
                distance = get_range()
                print("usound_sensor_dist=", distance)
                
                if distance > 1000 :
                    #possible d'avancer à fond
                    print("avancer à fond")
                    sleep(1)
                elif (distance <= 1000 and distance > 500):
                    #possible d'avancer très très vite
                    print("avancer très très vite")
                    sleep(1)
                elif (distance <=500 and distance > 200):
                    #possible d'avancer très vite
                    print("avancer très vite")
                    sleep(1)
                elif (distance <=200 and distance > 80):
                    #possible d'avancer vite
                    print("avancer vite")
                    sleep(1)
                elif (distance <=80 and distance > 45):
                    #possible d'avancer lentement
                    print("avancer lentement")
                    sleep(1)
                elif (distance <=45 and distance > 15):
                    #possible d'avancer très lentement
                    print("avancer très lentement")
                    sleep(1)
                elif (distance <= 15 and distance >= 0):
                    #pas possible d'avancer
                    print("pas possible d'avancer")
                    sleep(1)

                else: # si erreur de mesure de distance
                    stop()
                    print("stop pour erreur avec la distance mesurée")
                    sleep(1)
            nb_measures -= 1

    stop()
    clean()
