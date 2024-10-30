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

torque_cof = my_drive.axis0.motor.config.torque_constant * 16
print("torque_cof is " + str(torque_cof))
my_drive.axis0.config.general_lockin.current= 4.5
my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL	
my_drive.axis0.controller.input_torque = 0
print("my_drive.axis0.controller.config.control_mode = AXIS_STATE_CLOSED_LOOP_CONTROL")
time.sleep(1)

oscilloscope_data =[]
setpoint_data =[]
direction = 1
MAX_CURRENT = 60
calib_scan_distance = MAX_CURRENT*torque_cof
calib_torque_ramp = 0.2
calibration_max_steps = int( calib_scan_distance / calib_torque_ramp )
# for step in range(0,calibration_max_steps):
#     my_drive.axis0.controller.input_torque = direction*step *calib_scan_distance/calibration_max_steps
#     setpoint_data.append(MAX_CURRENT*step *1/calibration_max_steps)
#     time.sleep(0.003)
#     oscilloscope_data.append(my_drive.axis0.motor.current_control.Iq_measured)


# for step in range(0,calibration_max_steps):
#     my_drive.axis0.controller.input_torque = calib_scan_distance - direction*step *calib_scan_distance/calibration_max_steps
#     setpoint_data.append(MAX_CURRENT*step *1/calibration_max_steps)
#     time.sleep(0.001)
#     oscilloscope_data.append(my_drive.axis0.motor.current_control.Iq_measured)

direction = -1
for step in range(0,calibration_max_steps):
    my_drive.axis0.controller.input_torque = direction*step *calib_scan_distance/calibration_max_steps
    setpoint_data.append(MAX_CURRENT*step *1/calibration_max_steps)
    time.sleep(0.002)
    oscilloscope_data.append(my_drive.axis0.motor.current_control.Iq_measured)

# for step in range(0,calibration_max_steps):
#     my_drive.axis0.controller.input_torque = direction*calib_scan_distance - direction*step *calib_scan_distance/calibration_max_steps
#     setpoint_data.append(MAX_CURRENT*step *1/calibration_max_steps)
#     time.sleep(0.001)
#     oscilloscope_data.append(my_drive.axis0.motor.current_control.Iq_measured)



my_drive.axis0.controller.input_torque = 0

# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

time.sleep(0.2)

for set_item,osc_item  in zip(setpoint_data, oscilloscope_data):
    print(f"Setpoint: {set_item},Oscilloscope: {osc_item}")



with open('output__actual_velocity.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(setpoint_data )


x = list(range(0,calibration_max_steps))
plt.plot(x,oscilloscope_data)

plt.show()