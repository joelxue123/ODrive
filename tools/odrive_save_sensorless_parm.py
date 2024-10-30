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
time.sleep(1)
my_drive.axis0.encoder.config.mode = ENCODER_MODE_INCREMENTAL
print("my_drive.axis0.encoder.config.mode = ENCODER_MODE_INCREMENTAL")
my_drive.axis0.encoder.config.is_high_speed_encode_query_disabled = True
print("my_drive.axis0.encoder.config.is_high_speed_encode_query_disabled = True")
my_drive.axis0.controller.config.vel_gain = 0.01
print("my_drive.axis0.controller.config.vel_gain = 0.01")
my_drive.axis0.controller.config.vel_integrator_gain = 0.05
print("y_drive.axis0.controller.config.vel_integrator_gain = 0.05")
my_drive.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL	
print("my_drive.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL")
my_drive.axis0.controller.config.vel_limit = 100
print("my_drive.axis0.controller.config.vel_limit = 100")
my_drive.axis0.motor.config.current_lim =15
print("my_drive.axis0.motor.config.current_lim =15")
my_drive.axis0.motor.config.direction = 1   
print("my_drive.axis0.motor.config.direction = 1 ")
my_drive.axis0.sensorless_estimator.config.pm_flux_linkage = 0.084/21/1.5 
print("my_drive.axis0.sensorless_estimator.config.pm_flux_linkage = 0.084/21/1.5   ")
my_drive.axis0.motor.config.phase_resistance = 0.7
print("my_drive.axis0.motor.config.phase_resistance = 0.26")
my_drive.axis0.motor.config.phase_inductance = 0.0006
print("my_drive.axis0.motor.config.phase_inductance = 0.00006")
my_drive.axis0.motor.config.pre_calibrated = True
print("my_drive.axis0.motor.config.pre_calibrated = True")
my_drive.axis0.requested_state = AXIS_STATE_SENSORLESS_CONTROL	
print("my_drive.axis0.requested_state = AXIS_STATE_SENSORLESS_CONTROL")
my_drive.axis0.config.startup_sensorless_control = True	
print("my_drive.axis0.config.startup_sensorless_control = True	")
my_drive.save_configuration()
print("my_drive.save_configuration()")
time.sleep(3)
# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

time.sleep(0.2)
