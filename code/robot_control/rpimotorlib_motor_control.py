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
Motor control with module RpiMotorLib.py class L298NMDc, 
using threading to run four motors at same time.
Use push button(to VCC) on GPIO 17 to stop motors if necessary.

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




import time 
import RPi.GPIO as GPIO
from RpiMotorLib import rpi_dc_lib
import concurrent.futures

# ====== tests for  DC motor L298 ====
# ena - - 26
# in1 - - 19
# in2 - - 13
# in3 - - 21
# in4 - - 20
# enB - - 16

# ======== test motor 1 ==================

def motorone():
    
    print(" TEST: testing motor 1") 
    # Motorssetup
    MotorOne = rpi_dc_lib.L298NMDc(19 ,13 ,26 ,50 ,True, "motor_one")

    # ================ Motors one test  section 1=============
    try:
        print("1. motor forward")
        MotorOne.forward(15)
        input("press key to stop") 
        print("motor stop\n")
        MotorOne.stop(0)
        time.sleep(3)

        print("2. motor forward speed up")
        for i in range(15,30):
            MotorOne.forward(i)
            time.sleep(1)
        MotorOne.stop(0)
        print("motor stoped\n")
        time.sleep(3)
        
        print("3. motor backward")
        MotorOne.backward(15)
        input("press key to stop") 
        MotorOne.stop(0)
        print("motor stopped\n")
        time.sleep(3)

        print("4. motor backward speed up")
        for i in range(15,30):
            MotorOne.backward(i)
            time.sleep(1)
        MotorOne.stop(0)
        print("motor stopped\n")
        time.sleep(3)
         
        print("5  brake check")
        MotorOne.forward(50)
        time.sleep(3)
        MotorOne.brake(0)
        print("motor brake\n")
      
    except KeyboardInterrupt:
            print("CTRL-C: Terminating program.")
    except Exception as error:
            print(error)
            print("Unexpected error:")
    finally:
        MotorOne.cleanup(False)

    
def motortwo():
      
    print(" TEST: testing motor ") 
    # Motorssetup
    MotorTwo = rpi_dc_lib.L298NMDc(21 ,20 ,16 ,50 ,True, "motor_two")

    # ================ Motors two test  section 1=============
    try:
        print("1. motor forward")
        MotorTwo.forward(15)
        input("press key to stop") 
        MotorTwo.stop(0)
        print("motor stop\n")
        time.sleep(3)
       

        print("2. motor forward speed up")
        for i in range(15,30):
            MotorTwo.forward(i)
            time.sleep(1)
        MotorTwo.stop(0)
        print("motor stop\n")
        time.sleep(3)  
          
        
        print("3. motor backward")
        MotorTwo.backward(15)
        input("press key to stop") 
        MotorTwo.stop(0)
        print("motor stop\n")
        time.sleep(3)
        

        print("4. motor backward speed up")
        for i in range(15,30):
            MotorTwo.backward(i)
            time.sleep(1)
        MotorTwo.stop(0)
        print("motor stop\n")
        time.sleep(3)
        
         
        print("5 .brake check")
        MotorTwo.forward(50)
        time.sleep(3)
        MotorTwo.brake(0)
        print("motor brake\n")
        
    except KeyboardInterrupt:
            print("CTRL-C: Terminating program.")
    except Exception as error:
            print(error)
            print("Unexpected error:")
    finally:
        MotorTwo.cleanup(True)
    
# ===================MAIN===============================

if __name__ == '__main__':
   
    print("START")
    print("motorone tests")
    motorone()
    time.sleep(3)
    print("motortwo tests")
    motortwo()
    exit()
    

# =====================END===============================
