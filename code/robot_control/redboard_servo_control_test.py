from redboard import RedBoard
import inquirer
import asyncio
from time import sleep

# Define Motor Control
r = RedBoard()

# Parallax Continuous Rotation Servo Communication Protocol: 
# 1.3 ms Full speed clockwise, 1.5 ms No rotation, 1.7 ms Full speed counter-clockwise
r.s20_config = 1300, 1700
r.s21_config = 1700, 1300

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
	sleep(1.25)	# Calibrated to time of turning 90 degrees
	move_forward()

def stop_movement():
	r.s20 = 0
	r.s21 = 0

# Movement order
def slave(order):
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

question = [inquirer.List('direction', message="Select direction", choices=['forward', 'backward', 'left', 'right', 'stop'], ),]

async def loop():
	while True:
		answer = inquirer.prompt(question)
		order = answer["direction"]
		slave(order)
		await asyncio.sleep(0)

async def init_main():
	await loop()  # Enter main loop of program

	transport.close()  # Clean up serve endpoint

if __name__=='__main__':
	print("Awaiting order...")
	asyncio.run(init_main())