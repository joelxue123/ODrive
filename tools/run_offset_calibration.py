#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math
import matplotlib.pyplot as plt
import csv
import csv
import qdd_tests
# Find a connected ODrive (this will block until you connect one)




print("finding an odrive...")
my_drive = odrive.find_any()
time.sleep(1)
my_drive.axis0.requested_state = AXIS_STATE_IDLE
time.sleep(0.1)
my_drive.axis0.config.enable_watchdog = False
qdd_tests.qdd_test(my_drive)
my_drive.axis0.clear_errors()
my_drive.axis0.requested_state = AXIS_STATE_IDLE
time.sleep(0.1)
my_drive.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
my_drive.axis0.motor.config.calibration_current = 30
time.sleep(1)

my_drive.axis0.encoder.config.pre_calibrated = False

for i in range(0, 100000):
    run_calibration_read =  my_drive.axis0.encoder.is_ready
    if run_calibration_read == True:
        my_drive.axis0.encoder.config.pre_calibrated = True
        print("Encoder offset calibration done")
        break

    erro = my_drive.axis0.error
    if erro != 0:
        print("Error: ", erro)
        break

    time.sleep(0.1)





