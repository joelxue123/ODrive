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
    if len(sys.argv) > 1:
        input_can_id = sys.argv[1]

    if not input_can_id.isdigit():
        raise ValueError("Invalid CAN ID. Please provide a valid CAN ID.")

    # Find a connected ODrive (this will block until you connect one)
    print("finding an odrive...")
    my_drive = odrive.find_any()

    # To read a value, simply read the property
    print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

    time.sleep(0.2)

    can_id = my_drive.axis0.config.can_node_id
    logging.info(f"old can_id: {can_id}")

    my_drive.axis0.config.can_node_id = input_can_id
    can_id = my_drive.axis0.config.can_node_id
    logging.info(f"new can_id: {can_id}")

    time.sleep(1)