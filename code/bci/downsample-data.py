# downsample-data.py
# Downsample Data Example from https://brainflow.readthedocs.io/en/stable/Examples.html#python-downsample-data
# 20 dataframes are read and downsampled to 6-10 frames

import time
import numpy as np

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


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
    data = board.get_board_data(250) # 1 second?
    board.stop_stream()
    board.release_session()

    eeg_channels = BoardShim.get_eeg_channels(board_id)
    #print(type(eeg_channels))
    # demo for downsampling, it just aggregates data
    for count, channel in enumerate(eeg_channels[:5]):
        print('Original data for channel %d:' % channel)
        print(len(data[channel]))
        if count == 0:
            downsampled_data = DataFilter.perform_downsampling(data[channel], 10, AggOperations.MEDIAN.value)
        elif count == 1:
            downsampled_data = DataFilter.perform_downsampling(data[channel], 10, AggOperations.MEAN.value)
        else:
            downsampled_data = DataFilter.perform_downsampling(data[channel], 10, AggOperations.EACH.value) # 10 downsampling periods
        print('Downsampled data for channel %d:' % channel)
        print(len(downsampled_data))
        print(downsampled_data)


if __name__ == "__main__":
    main()