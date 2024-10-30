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

torque_cof = my_drive.axis0.motor.config.torque_constant
print("torque_cof is " + str(torque_cof))
my_drive.axis0.config.general_lockin.current= 4.5
my_drive.axis0.controller.config.control_mode = CONTROL_MODE_PVT_CONTROL
my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL	
my_drive.axis0.controller.input_torque = 0
print("my_drive.axis0.controller.config.control_mode = AXIS_STATE_CLOSED_LOOP_CONTROL")
time.sleep(2)


my_drive.axis0.controller.input_torque = 0

# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

time.sleep(0.2)



plt.show()