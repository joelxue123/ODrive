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
# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()

# Calibrate motor and wait for it to finish
print("starting calibration...")

# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

my_drive.axis0.motor.capturing =1
time.sleep(0.2)
oscilloscope_data =[]

for oscilloscope_item in range(0,4095):
    #print("oscilloscope_item " + str(oscilloscope_item) + " = " + str(my_drive.get_oscilloscope_val(oscilloscope_item)))
    oscilloscope_data.append(my_drive.get_oscilloscope_val(oscilloscope_item))

for item in   oscilloscope_data:
    print( item)

with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(oscilloscope_data)

x = list(range(0,4095))
plt.plot(x,oscilloscope_data)

plt.show()
