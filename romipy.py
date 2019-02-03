#!/usr/bin/python3
# -*- coding:Utf-8 -*-

from time import sleep
from engines import *
from obstacle_detection import *
from qmc5883l import *

#________________MAIN_______________________#

#test_engines()
#test_obstacle_detection(50)

magnetometer = I2c_qmc5883l()
sleep(0.1)
magnetometer.read_status()
sleep(0.1)
magnetometer.read_config()
sleep(0.1)
magnetometer.read_config2()
sleep(0.1)
magnetometer.read_temp()
sleep(0.1)
magnetometer.read_xyz()
sleep(0.5)

print(magnetometer)

print("fermeture...")
sleep(5)
