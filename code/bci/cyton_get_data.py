# cyton_get_data.py
from time import sleep
import pprint

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
#from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

def main():
    #BoardShim.enable_dev_board_logger()

    params = BrainFlowInputParams()
    params.serial_port = 'COM4'
    board_id = BoardIds.CYTON_BOARD.value # Use SYNTHETIC_BOARD for demo
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream(45000, 'file://cyton_data.csv:w') # TODO What is the actual transfer rate?
    sleep(10) # Collect data for 10 seconds
    #data = board.get_board_data() 
    board.stop_stream()
    board.release_session()

    #print(data)
    pprint.pprint(board.get_board_descr(board_id)) # Pretty-print json

if __name__ == "__main__":
    main()