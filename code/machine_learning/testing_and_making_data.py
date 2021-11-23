# Uses LSL between EEG Headset and Computer, and OSC between Computer and RPi
# Saves LSL stream to /data, inferes stream towards model, and sends result over OSC.
#
# Forked from https://github.com/Sentdex/BCI/
#
# TODO Consider the common spatial patterns approach, https://en.wikipedia.org/wiki/Common_spatial_pattern , is used specifically for this task and is relatively simple to implement. Using wavelets

from pylsl import StreamInlet, resolve_stream
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib import style
from collections import deque
import cv2
import os
import random
import tensorflow as tf
from pythonosc.udp_client import SimpleUDPClient

# OSC 
# Send direction to Robot by OSC

ip = "192.168.1.25" #"192.168.1.70"# IP of the OSC receiver
port = 1337 # Port the OSC receiver is listening on
client = SimpleUDPClient(ip, port)  # Create client

direction = ['forward', 'backward', 'left', 'right', 'stop']

def send_direction(address, order):
    pass


MODEL_NAME = "new_models/36.45-acc-64x3-batch-norm-9epoch-1635863283-loss-56.5.model"  # your model path here

model = tf.keras.models.load_model(MODEL_NAME)
reshape = (-1, 5, 60) # 5 channels
model.predict( np.zeros((32,5,60)).reshape(reshape) )

ACTION = 'right' # THIS IS THE ACTION YOU'RE THINKING. Data saved in directory named by action # TODO Option to trow away recorded data

FFT_MAX_HZ = 60

HM_SECONDS = 10  # this is approximate. Not 100%. do not depend on this.
TOTAL_ITERS = HM_SECONDS*25  # ~25 iters/sec TODO Not accurate - use time.time checks
BOX_MOVE = "model"  # random or model

last_print = time.time()
fps_counter = deque(maxlen=150)

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'FFT') # Note stream name 'FFT' must correspond to LSL sender
# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

WIDTH = 800
HEIGHT = 800
SQ_SIZE = 50
MOVE_SPEED = 10 # Speed of square[]

square = {'x1': int(int(WIDTH)/2-int(SQ_SIZE/2)), 
          'x2': int(int(WIDTH)/2+int(SQ_SIZE/2)),
          'y1': int(int(HEIGHT)/2-int(SQ_SIZE/2)),
          'y2': int(int(HEIGHT)/2+int(SQ_SIZE/2))}


box = np.ones((square['y2']-square['y1'], square['x2']-square['x1'], 3)) * np.random.uniform(size=(3,))
horizontal_line = np.ones((HEIGHT, 10, 3)) * np.random.uniform(size=(3,))
vertical_line = np.ones((10, WIDTH, 3)) * np.random.uniform(size=(3,))

total = 0
left = 0
right = 0
none = 0
correct = 0 

channel_datas = []

for i in range(TOTAL_ITERS):  # how many iterations. TODO while True: "howto gracefully end while loop?" if keypress break?
    channel_data = []
    for i in range(5): # For each of the channels
        sample, timestamp = inlet.pull_sample()
        channel_data.append(sample[:FFT_MAX_HZ]) # Trow away frequencies over 60

    fps_counter.append(time.time() - last_print)
    last_print = time.time()
    cur_raw_hz = 1/(sum(fps_counter)/len(fps_counter))
    print(cur_raw_hz)

    env = np.zeros((WIDTH, HEIGHT, 3))

    env[:,HEIGHT//2-5:HEIGHT//2+5,:] = horizontal_line
    env[WIDTH//2-5:WIDTH//2+5,:,:] = vertical_line
    env[square['y1']:square['y2'], square['x1']:square['x2']] = box

    cv2.imshow('', env)
    cv2.waitKey(1)

    network_input = np.array(channel_data).reshape(reshape)
    out = model.predict(network_input)
    print(out[0])

    if BOX_MOVE == "random":
        move = random.choice([-1,0,1])
        square['x1'] += move
        square['x2'] += move

    elif BOX_MOVE == "model":
        choice = np.argmax(out)
        if choice == 0:
            if ACTION == "left":
                correct += 1
            square['x1'] -= MOVE_SPEED
            square['x2'] -= MOVE_SPEED
            left += 1
            print("Direction: left")
            osc_message = 'left'
            client.send_message("/openbci", osc_message) # Send string message
            # TODO def send_direction(args): print, osc_msg = dir[args], client.send

        elif choice == 2:
            if ACTION == "right":
                correct += 1
            square['x1'] += MOVE_SPEED
            square['x2'] += MOVE_SPEED
            right += 1
            print("Direction: right")
            osc_message = 'right'
            client.send_message("/openbci", osc_message) # Send string message

        else:
            if ACTION == "none":
                correct += 1
            none += 1
            print("Direction: stop")
            osc_message = 'stop'
            client.send_message("/openbci", osc_message) # Send string message

    total += 1


    channel_datas.append(channel_data)

datadir = "data"
if not os.path.exists(datadir):
    os.mkdir(datadir)

actiondir = f"{datadir}/{ACTION}"
if not os.path.exists(actiondir):
    os.mkdir(actiondir)

print(len(channel_datas))

print(f"saving {ACTION} data...")
np.save(os.path.join(actiondir, f"{int(time.time())}.npy"), np.array(channel_datas))
print("done.")

for action in ['left', 'right', 'none']:
    #print(f"{action}:{len(os.listdir(f'data/{action}'))}")
    print(action, sum(os.path.getsize(f'data/{action}/{f}') for f in os.listdir(f'data/{action}'))/1_000_000, "MB")

print(ACTION, correct/total)
print(f"left: {left/total}, right: {right/total}, none: {none/total}")

with open("accuracies.csv", "a") as f:
    f.write(f"{int(time.time())},{ACTION},{correct/total},{MODEL_NAME},{left/total},{right/total},{none/total}\n")