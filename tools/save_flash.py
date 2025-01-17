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
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()
time.sleep(1)
axis_error = my_drive.axis0.error
motor_error = my_drive.axis0.motor.error
encoder_error = my_drive.axis0.encoder.error

#my_drive.axis0.config.can_node_id =2
can_id = my_drive.axis0.config.can_node_id
logging.info(f"can_id: {can_id}")

logging.info(f"Axis error: {axis_error}")
logging.info(f"Motor error: {motor_error}")
logging.info(f"Encoder error: {encoder_error}")

my_drive.axis0.config.current_base = 70
logging.info(f"current_base: {my_drive.axis0.config.current_base}")

my_drive.axis0.motor.config.motor_torque_base = 70
logging.info(f"motor_torque_base: {my_drive.axis0.motor.config.motor_torque_base}")

my_drive.axis0.config.enable_watchdog = True
my_drive.save_configuration()
print("my_drive.save_configuration()")
time.sleep(3)
# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

time.sleep(0.2)
