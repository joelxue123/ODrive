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
my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL	
my_drive.axis0.controller.input_torque = 0
print("my_drive.axis0.controller.config.control_mode = AXIS_STATE_CLOSED_LOOP_CONTROL")
time.sleep(2)

oscilloscope_data =[]
setpoint_data =[]
calib_scan_distance = 4.5*torque_cof
calib_scan_omega = 0.0002
calibration_max_steps = int( calib_scan_distance / calib_scan_omega )
for step in range(0,calibration_max_steps):
    my_drive.axis0.controller.input_torque = step *calib_scan_distance/calibration_max_steps
    setpoint_data.append(4.5*step *1/calibration_max_steps)
    time.sleep(0.001)
    oscilloscope_data.append(my_drive.axis0.encoder.pos_abs)


# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

time.sleep(0.2)

for item in   oscilloscope_data:
    print( item)


with open('output__actual_velocity.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(setpoint_data )


x = list(range(0,calibration_max_steps))
plt.plot(x,setpoint_data)

plt.show()