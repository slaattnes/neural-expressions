# psd_welch_data.py
# Get PSD Welch Data Example from https://brainflow.readthedocs.io/en/stable/Examples.html#python-band-power

import time
import numpy as np

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations


def main():
    BoardShim.enable_dev_board_logger()

    # use SYNTHETIC_BOARD for demo
    params = BrainFlowInputParams()
    params.serial_port = 'COM4'
    board_id = BoardIds.SYNTHETIC_BOARD.value
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(10)

    sampling_rate = BoardShim.get_sampling_rate(board_id)
    nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
    window_size = 4
    num_points = window_size * sampling_rate
    data = board.get_board_data(num_points)
    
    board.stop_stream()
    board.release_session()

    eeg_channels = BoardShim.get_eeg_channels(board_id)
    #print(type(eeg_channels))

    # Get PSD Welch data
    for count, channel in enumerate(eeg_channels[:5]):
        psd_data = DataFilter.get_psd_welch(data[channel], nfft, nfft // 2, sampling_rate,
                                   WindowFunctions.BLACKMAN_HARRIS.value) #Returns amplitude and frequency arrays of len N / 2 + 1

        print(f'Amplitude, channel {channel} %s' %psd_data[0])
        print(f'Frequency, channel {channel} %s' %psd_data[1])
        #break # Break for printing just the first channel
    
    print(f'Amplitude, {len(psd_data[0])} datapoints')
    print(f'Frequency, {len(psd_data[1])} datapoints')
        
if __name__ == "__main__":
    main()