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

    print("finding an odrive...")
    my_drive = odrive.find_any()
    can_id = my_drive.axis0.config.can_node_id
    logging.info(f"can_id: {can_id}")
    my_drive.axis0.requested_state = AXIS_STATE_IDLE
    time.sleep(0.1)

    while True:
        board_temperture_voltage  = my_drive.get_adc_voltage(14) 
        logging.info(f"board_temperture_voltage: {board_temperture_voltage}")
        board_temperture = my_drive.axis0.fet_thermistor.temperature
        logging.info(f"board_temperture: {board_temperture}")

        motor_temperture_voltage = my_drive.get_adc_voltage(15) 
        logging.info(f"motor_temperture_voltage: {motor_temperture_voltage}")
        motor_temperture = my_drive.axis0.fet_thermistor.aux_temperature
        logging.info(f"motor_temperture: {motor_temperture}")
        logging.info("waitting 1s **********************************")

        time.sleep(1)
