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

motor_encoder   = 1
gear_encoder   = 2

encoder_type = gear_encoder


if encoder_type == motor_encoder:
    velocity = 20
elif encoder_type == gear_encoder:
    velocity = 150




print("finding an odrive...")
my_drive = odrive.find_any()
time.sleep(1)
my_drive.axis0.requested_state = AXIS_STATE_IDLE
time.sleep(0.1)

qdd_tests.qdd_test(my_drive)
time.sleep(0.1)
my_drive.axis0.config.enable_watchdog = False
my_drive.axis0.config.general_lockin.current = 15
my_drive.axis0.config.general_lockin.vel = velocity
my_drive.axis0.encoder.config.is_high_speed_encode_query_enabled = False
my_drive.axis0.clear_errors()
time.sleep(0.1)
my_drive.axis0.requested_state = AXIS_STATE_LOCKIN_SPIN
time.sleep(5)

