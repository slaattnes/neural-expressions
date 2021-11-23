# code/rpi_motor_control.py

# Motor Control Library: https://github.com/ApproxEng/RedBoard
from redboard import RedBoard, Display

# Open Sound Control Library in Concurrent Mode so not to block main program loop
# https://python-osc.readthedocs.io/en/latest/server.html#concurrent-mode
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher

import asyncio
from time import sleep


# Define Motor Control & OLED
r = RedBoard()
d = Display()

d.text("       ⊂(◉‿◉)⊃", 
        "Wherever we're going,", 
        "we're going together...")

# Parallax Continuous Rotation Servo Communication Protocol: 
# 1.3 ms Full speed clockwise, 1.5 ms No rotation, 1.7 ms Full speed counter-clockwise
r.s20_config = 1300, 1700
r.s21_config = 1700, 1300 # Left-Right logic switch

# Define movements
def move_forward():
    r.s20 = 1
    r.s21 = 1

def move_backward():
    r.s20 = -1
    r.s21 = -1

def turn_left(): # Turn left, then forward
    r.s20 = 0
    r.s21 = 1
    sleep(1.25) # Calibrated to time of turning 90 degrees
    move_forward()

def turn_right(): # Turn right, then forward
    r.s20 = 1
    r.s21 = 0
    sleep(1.25) # Calibrated to time of turning 90 degrees
    move_forward()

def stop_movement():
    r.s20 = 0
    r.s21 = 0

# OSC Receive Mental Imagery of movements
def osc_message(address, order):
    print(order)
    if order == "forward":
        move_forward()
    elif order == "backward":
        move_backward()
    elif order == "left":
        turn_left()
    elif order == "right":
        turn_right()
    else:
        stop_movement()

dispatcher = Dispatcher()
dispatcher.map("/openbci", osc_message)

ip = "0.0.0.0" # Listen for OSC sender from everywhere
port = 1337 # Port the OSC sender is using

async def loop():
    while True:
        await asyncio.sleep(0)

async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint

if __name__=='__main__':
    print("Awaiting order...")
    asyncio.run(init_main())