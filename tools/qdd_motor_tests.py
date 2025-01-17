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
# Find a connected ODrive (this will block until you connect one)



print("finding an odrive...")
my_drive = odrive.find_any()
time.sleep(1)


axis_error = my_drive.axis0.error
motor_error = my_drive.axis0.motor.error
encoder_error = my_drive.axis0.encoder.error

print("axis error: ", axis_error)
print("motor error: ", motor_error)
print("encoder error: ", encoder_error)

motor_test_failed  = motor_error + encoder_error

kp_gain = my_drive.axis0.kp_gain
kd_gain = my_drive.axis0.kd_gain

if kp_gain != 1 or kd_gain != 1:
    print("kp_gain or kd_gain is not 1")
    exit()

if motor_test_failed == 0:
    print("motor test passed")
    my_drive.axis0.config.enable_watchdog = False
    my_drive.axis0.clear_errors()
    time.sleep(0.1)
    my_drive.axis0.motor.using_old_torque_constant = False
    my_drive.axis0.controller.input_torque = 1
    my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    time.sleep(3)
    my_drive.axis0.requested_state = AXIS_STATE_IDLE
else:
    print("motor test failed")


