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


my_drive.axis0.config.general_lockin.current= 10
my_drive.axis0.config.general_lockin.ramp_distance = 0
my_drive.axis0.config.general_lockin.vel = 0
my_drive.axis0.requested_state = AXIS_STATE_LOCKIN_SPIN	
print("my_drive.axis0.controller.config.control_mode = AXIS_STATE_LOCKIN_SPIN")
time.sleep(4)

oscilloscope_data =[]
setpoint_data =[]
calib_scan_distance = 2*math.pi*21
calib_scan_omega = 0.03
calibration_max_steps = int( calib_scan_distance / calib_scan_omega )
for step in range(0,calibration_max_steps):
    my_drive.axis0.config.general_lockin.ramp_distance = step *calib_scan_distance/calibration_max_steps
    setpoint_data.append(65535*step *1/calibration_max_steps)
    time.sleep(0.005)
    oscilloscope_data.append(my_drive.axis0.encoder.pos_abs)


# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

time.sleep(0.2)

for item in   oscilloscope_data:
    print( item)

offset = oscilloscope_data[0]    
for step in   range(0,calibration_max_steps):
    oscilloscope_data[step] = oscilloscope_data[step] -  offset
    if oscilloscope_data[step] <=0 :
        oscilloscope_data[step] = oscilloscope_data[step] + 65535


errro_data = []
for step in   range(0,calibration_max_steps):
    err0 = (setpoint_data[step] - oscilloscope_data[step]) *360/65535
    while err0 >= 360:
        err0 =err0 - 360
    while err0 <= -360:
        err0 =err0 + 360
    errro_data.append(err0)

with open('output__actual_velocity.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(errro_data )


x = list(range(0,calibration_max_steps))
plt.plot(x,errro_data )

plt.show()