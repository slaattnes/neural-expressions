# Neural Expressions

Experimentations with Brain-to-Sculpture communication and EEG actuated robotic sculptures

## Directory structure

 * [README.md](./README.md) This file
 * [notebook.ipynb](./notebook.ipynb) Showcase and notebook over the project
 * [code](./code)
   * [requirements.txt](./code/requirements.txt) Python libraries needed, python 3.8 used
   * [bci](./code/bci)
     * [cyton_get_data.py](./code/bci/cyton_get_data.py) Simple test with brainflow library for streaming EEG data to computer and getting EEG board information
     * [lslStreamTest.py](./code/bci/lslStreamTest.py) Tests for LSL stream, forked from https://github.com/OpenBCI/OpenBCI_GUI/tree/master/Networking-Test-Kit
     * [brainflow](./code/bci/brainflow) Brainflow library. Not needed with 'pip install brainflow'
   * [robot_control](./code/robot_control)
     * [osc_send.py](./code/robot_control/osc_send.py) Testing OSC messaging from computer via clt
     * [osc_receive.py](./code/robot_control/osc_receive.py) Testing reception of OSC messages 
     * [redboard.py](./code/robot_control/redboard.py) Redboard library. Not needed with 'pip install redboard'
     * [redboard_servo_control_test.py](./code/robot_control/redboard_servo_control_test.py) Stand-alone cli script for testing motor control
     * [redboard_servo_control.py](./code/robot_control/redboard_servo_control.py) Simple functions for redboard library for moving a 2-wheeled robot car based on received OSC messages
     * [rpimotorlib_motor_control.py](./code/robot_control/[rpimotorlib_motor_control.py) Unfinished script for motor control with RpiMotorLib library
     * [rpimotorlib_stepper_control.py](./code/robot_control/rpimotorlib_stepper_control.py) Unfinished script for stepper control with RpiMotorLib library
   * [machine_learning](./code/machine_learning)
     * [get_npydata.py](./code/machine_learning/get_npydata.py) Saves LSL stream as 3-dimensional numpy array ( [stream][channels][amplitude] )
     * [CytonUserSettings.json](./code/machine_learning/CytonUserSettings.json) Just for reference: Settings used in OpenBCI GUI
     * [data](./code/machine_learning/data) Numpy arrays with FFT stream from EEG recordings saved as binary in [Unix time].npy files 
       * [left](./code/machine_learning/data/left)
       * [none](./code/machine_learning/data/none)
       * [right](./code/machine_learning/data/right)
     * [testing_and_making_data.py](./code/machine_learning/testing_and_making_data.py) Saves LSL stream to /data, inferes stream towards model, and sends result over OSC. Forked from https://github.com/Sentdex/BCI/
     * [accuracies.csv](./code/machine_learning/accuracies.csv) Record over accuracy of models, generated by testing_and_making_data.py
     * [traning.py](./code/machine_learning/training.py) Trains data on 1D Convolutional network, saves models for each epoch in /new_models
     * [new_models](./code/machine_learning/new_models)
     * [validation_data](./code/machine_learning/validation_data) Validation data excluded from /data
       * [left](./code/machine_learning/validation_data/left)
       * [none](./code/machine_learning/validation_data/none)
       * [right](./code/machine_learning/validation_data/right)
     * [analysis.py](./code/machine_learning/analysis.py) Tests model by comparing predicted action vs action thought, and produces a confusion matrix
     * [models](./code/machine_learning/models) Stored best-of models
 * [img](./img) Images used in [jupyter notebook](./notebook.ipynb)
 * [LICENSE.md](./LICENSE.md) Copyright information

## License

MIT License Copyright © 2021 Daniel Slåttnes