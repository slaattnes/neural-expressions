'''Simple test for receiving OSC messages'''
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio

def osc_message(address, order):
	print(order)

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