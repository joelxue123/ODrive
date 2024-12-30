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

while 1:
    pos_deg = my_drive.axis0.encoder.gear_pos_deg
    print("pos deg is " + str(pos_deg) + "°")
    time.sleep(1)
