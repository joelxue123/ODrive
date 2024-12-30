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
my_drive.axis0.requested_state = AXIS_STATE_IDLE
time.sleep(0.1)

my_drive.axis0.config.enable_watchdog = False
my_drive.axis0.config.general_lockin.current = 5
my_drive.axis0.config.general_lockin.vel = 120
my_drive.axis0.encoder.config.is_high_speed_encode_query_enabled = False
my_drive.axis0.clear_errors()
#my_drive.axis0.requested_state = AXIS_STATE_LOCKIN_SPIN
