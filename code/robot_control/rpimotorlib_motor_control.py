# SPDX-FileCopyrightText: 2021 Daniel Slåttnes daniel@slaattnes.com
#
# SPDX-License-Identifier: MIT

# Creature Subroutines for interconnection with Brain Waves
# 
# Brainflow API library is used for reading brain waves with a OpenBCI Cyton Electroencephalography (EEG) device.
#
# Motor library is used for motor control of V-TEC 6V worm gear 160 RPM motors + L298N H-bridge modules.
#
# DC motors actuate wire-driven tentacle based on the input.
#
# Author: Daniel Slåttnes
# Based on https://github.com/gavinlyonsrepo/RpiMotorLib/blob/master/test/L298_DCMot_Test.py

#!/usr/bin/env python3
""" 
test example file for module:rpiMotorlib.py
file: RpiMotorLib.py class BYJMotor, 
use threading to run two motors at same time.
use push button(to VCC) on GPIO 17 to stop motors if necessary

"""

import time
import RPi.GPIO as GPIO
import concurrent.futures
from RpiMotorLib import RpiMotorLib

GPIO.setwarnings(False)
# For GPIO numbering, choose BCM or, for pin numbering, choose BOARD 
GPIO.setmode(GPIO.BCM)
# To Test motor stop, put push button to VCC on GPIO 17
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Motor control declaration of four named instance of class, name and type of motor
motorOne = RpiMotorLib.BYJMotor("BYJMotorOne", "28BYJ")
motorTwo = RpiMotorLib.BYJMotor("BYJMotorTwo", "28BYJ")
motorThree = RpiMotorLib.BYJMotor("BYJMotorThree", "28BYJ")
motorFour = RpiMotorLib.BYJMotor("BYJMotorFour", "28BYJ")

# Connect GPIO to [IN1 , IN2 , IN3 ,IN4] on Motor PCB
GpioPins1 = [18, 23, 24, 25]
GpioPins2 = [22, 27, 17, 4]
GpioPins3 = [19, 13, 6, 5]
GpioPins4 = [8, 7, 12, 16]

steps=128

clockwise = False
anticlockwise = True
direction=clockwise

def move_motorOne(steps=128, direction=clockwise):
    print(f"Motor One {direction}, {steps} steps")
    pass

def move_motorTwo(steps=128, direction=clockwise):
    print(f"Motor Two {direction}, {steps} steps")
    pass 

def move_motorThree(steps=128, direction=clockwise):
    print(f"Motor Three {direction}, {steps} steps")
    pass

def move_motorFour(steps=128, direction=clockwise):
    print(f"Motor Four {direction}, {steps} steps")
    pass


def main():
    """main function loop"""

    # To Test motor stop , put push button to VCC on GPIO 17
    #GPIO.add_event_detect(17, GPIO.RISING, callback=button_callback)

    # ====== tests for four motors ====
    # mymotortest.motor_run(GPIOPins, wait, steps, counterclockwise, verbose, steptype, initdelay)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(motorOne.motor_run, GpioPins1, .05, steps, direction, False, "full", .05)
        f2 = executor.submit(motorTwo.motor_run, GpioPins2, .05, steps, direction, False, "full", .05)
        f3 = executor.submit(motorThree.motor_run, GpioPins3, .05, steps, direction, False, "full", .05)
        f4 = executor.submit(motorFour.motor_run, GpioPins4, .05, steps, direction, False, "full", .05)

# Comment in for testing motor stop function
#def button_callback(channel):
#    print("Test file: Stopping motor")
#    mymotortestOne.motor_stop()
#    mymotortestTwo.motor_stop()


# ===================MAIN===============================

if __name__ == '__main__':

    print("START")
    main()
    GPIO.cleanup()
    print("END")
    exit()

# =====================END===============================