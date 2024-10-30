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



print("finding an odrive...")
my_drive = odrive.find_any()
time.sleep(1)
my_drive.erase_configuration()
print("my_drive.save_configuration()")