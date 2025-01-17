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
from enum import Enum
import sys
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':


    # Find a connected ODrive (this will block until you connect one)
    print("finding an odrive...")
    my_drive = odrive.find_any()

    # To read a value, simply read the property
    print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

    time.sleep(0.2)

    can_id = my_drive.axis0.config.can_node_id
    logging.info(f"old can_id: {can_id}")

    current_base = my_drive.axis0.config.current_base
    logging.info(f"current_base: {current_base}")

    motor_torque_base = my_drive.axis0.motor.config.motor_torque_base
    logging.info(f"motor_torque_base: {motor_torque_base}")
    time.sleep(1)