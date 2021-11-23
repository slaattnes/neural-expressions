'''Simple test for sending OSC messages'''
from pythonosc.udp_client import SimpleUDPClient
import inquirer

ip = "192.168.1.25" # IP of the OSC receiver
port = 1337 # Port the OSC receiver is listening on

client = SimpleUDPClient(ip, port)  # Create client

question = [inquirer.List('direction', message="Select direction", choices=['forward', 'backward', 'left', 'right', 'stop'], ),]

while True:
	#direction = input("Select direction (forward/backward/left/right/stop): ")
	answer = inquirer.prompt(question)
	print(answer["direction"])
	osc_message = answer["direction"]
	client.send_message("/openbci", osc_message) # Send string message