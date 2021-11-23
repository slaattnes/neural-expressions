# Run the OpenBCI GUI
# Set Networking mode to LSL (Lab Streaming Layer), set data type to FFT, and name type 'FFT' (name of the LSL stream this script looks for)
#
# Thanks to @Sentdex - Nov 2019 Forked from https://github.com/OpenBCI/OpenBCI_GUI/blob/master/Networking-Test-Kit/LSL/lslStreamTest_FFTplot.py
from pylsl import StreamInlet, resolve_stream
import numpy as np
import time
from collections import deque # Fast and memory-efficient list appending
import os

ACTION = 'right' # THIS IS THE ACTION YOU'RE THINKING. Data saved in directory named by action

FFT_MAX_HZ = 60

HM_SECONDS = 10  # this is approximate. Not 100%. do not depend on this.
TOTAL_ITERS = HM_SECONDS*25  # ~25 iters/sec

last_print = time.time()
fps_counter = deque(maxlen=150)

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'FFT')
# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

channel_datas = []

for i in range(TOTAL_ITERS):  # how many iterations. Eventually this would be a while True
    channel_data = []
    for i in range(5): # For each of the channels
        sample, timestamp = inlet.pull_sample()
        channel_data.append(sample[:FFT_MAX_HZ])

    fps_counter.append(time.time() - last_print)
    last_print = time.time()
    cur_raw_hz = 1/(sum(fps_counter)/len(fps_counter))
    print(cur_raw_hz)

    channel_datas.append(channel_data)

# Save EEG Data
datadir = "data"
if not os.path.exists(datadir):
    os.mkdir(datadir)

actiondir = f"{datadir}/{ACTION}"
if not os.path.exists(actiondir):
    os.mkdir(actiondir)

print(len(channel_datas))

print(f"saving {ACTION} data...")
np.save(os.path.join(actiondir, f"{int(time.time())}.npy"), np.array(channel_datas)) # [TOTAL_ITERS*fps_counter][channel_datas in range(5)]
print("done.")

for action in ['left', 'right', 'none']:
    #print(f"{action}:{len(os.listdir(f'data/{action}'))}")
    print(action, sum(os.path.getsize(f'data/{action}/{f}') for f in os.listdir(f'data/{action}'))/1_000_000, "MB")

print(ACTION)
print(f"left: {left/total}, right: {right/total}, none: {none/total}")