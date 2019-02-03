#!/usr/bin/python3
# -*- coding:Utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep

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

def forward(speed):
    pwm_motor1_backward.ChangeDutyCycle(0)
    pwm_motor2_backward.ChangeDutyCycle(0)
    pwm_motor1_forward.ChangeDutyCycle(speed)
    pwm_motor2_forward.ChangeDutyCycle(speed)
    

def backward(speed):
    pwm_motor1_forward.ChangeDutyCycle(0)
    pwm_motor2_forward.ChangeDutyCycle(0)
    pwm_motor1_backward.ChangeDutyCycle(speed)
    pwm_motor2_backward.ChangeDutyCycle(speed)

def rotation_left(speed):
    pwm_motor2_backward.ChangeDutyCycle(0) 
    pwm_motor1_forward.ChangeDutyCycle(0)
    pwm_motor1_backward.ChangeDutyCycle(speed) 
    pwm_motor2_forward.ChangeDutyCycle(speed)

def rotation_right(speed):
    pwm_motor1_backward.ChangeDutyCycle(0) 
    pwm_motor2_forward.ChangeDutyCycle(0)
    pwm_motor2_backward.ChangeDutyCycle(speed) 
    pwm_motor1_forward.ChangeDutyCycle(speed)

def turn_right(speed):
    pwm_motor1_backward.ChangeDutyCycle(0) 
    pwm_motor2_forward.ChangeDutyCycle(0)
    pwm_motor2_backward.ChangeDutyCycle(0) 
    pwm_motor1_forward.ChangeDutyCycle(speed)

def turn_left(speed):
    pwm_motor1_backward.ChangeDutyCycle(0) 
    pwm_motor1_forward.ChangeDutyCycle(0)
    pwm_motor2_backward.ChangeDutyCycle(0) 
    pwm_motor2_forward.ChangeDutyCycle(speed)

def turn_back_right(speed):
    pwm_motor1_backward.ChangeDutyCycle(0) 
    pwm_motor1_forward.ChangeDutyCycle(0)
    pwm_motor2_forward.ChangeDutyCycle(0) 
    pwm_motor2_backward.ChangeDutyCycle(speed)

def turn_back_left(speed):
    pwm_motor2_backward.ChangeDutyCycle(0) 
    pwm_motor1_forward.ChangeDutyCycle(0)
    pwm_motor2_forward.ChangeDutyCycle(0) 
    pwm_motor1_backward.ChangeDutyCycle(speed)

def stop():
    GPIO.output(MOTOR1_BACKWARD, 0)
    GPIO.output(MOTOR1_FORWARD, 0)
    GPIO.output(MOTOR2_BACKWARD, 0)
    GPIO.output(MOTOR2_FORWARD, 0)

def clean():
    GPIO.output(DONT_SLEEP_DRV8833, 0)
    sleep(5)
    GPIO.cleanup()
    

#________________TESTS_______________________#

def test_engines():
    """TEST ENGINES DEMO"""

    GPIO.output(DONT_SLEEP_DRV8833, 1)

    if  not GPIO.input(FAULT_DRV8833):
        print("ERROR FAULT_DRV8833")
    else:
        forward(40)
        sleep(2)

        backward(20)
        sleep(2)

        rotation_left(20)
        sleep(2)

        rotation_right(30)
        sleep(2)

        turn_right(30)
        sleep(2)

        turn_left(30)
        sleep(2)

        turn_back_right(30)
        sleep(1)

        turn_back_left(30)
        sleep(1)

    
    stop()
    clean()
