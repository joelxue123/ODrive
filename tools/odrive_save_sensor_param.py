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

spi_cs   = 1
rs485_cs  = 2


encode_type = ENCODER_MODE_SPI_ABS_RLS
spi_485_cs_select_pin = rs485_cs

HSV_60 = 1
HSV_120 = 2
motor_type = HSV_120

if motor_type == HSV_60:
    phase_resistance = 0.1
    phase_inductance = 0.00009
    torque_constant = 0.12
    pm_flux_linkage = 0.12/10/1.5 
    pole_pairs = 10
    gear_ratio = 20

elif motor_type == HSV_120:
    phase_resistance = 0.065
    phase_inductance = 0.000055
    torque_constant = 0.087
    pm_flux_linkage = 0.087/21/1.5 
    pole_pairs = 21
    gear_ratio = 16
    pass


# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()
time.sleep(1)
my_drive.axis0.encoder.config.abs_spi_cs_gpio_pin = spi_cs
print("my_drive.axis0.encoder.config.abs_spi_cs_gpio_pin = " + str(spi_cs) )
my_drive.axis0.encoder.config.abs_485_cs_gpio_pin = rs485_cs
print("my_drive.axis0.encoder.config.abs_485_cs_gpio_pin = " + str(rs485_cs) )
my_drive.axis0.encoder.config.mode = encode_type
print("my_drive.axis0.encoder.config.mode = " + str(encode_type) )
my_drive.axis0.encoder.config.is_high_speed_encode_query_enabled = True
print("my_drive.axis0.encoder.config.is_high_speed_encode_query_enabled = True")
my_drive.axis0.controller.config.vel_gain = 0.02
print("my_drive.axis0.controller.config.vel_gain = 0.01")
my_drive.axis0.controller.config.vel_integrator_gain = 0.01
print("y_drive.axis0.controller.config.vel_integrator_gain = 0.05")
my_drive.axis0.controller.config.control_mode = CONTROL_MODE_PVT_CONTROL	
print("my_drive.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL")
my_drive.axis0.controller.config.vel_limit = 40
print("my_drive.axis0.controller.config.vel_limit = 100")
my_drive.axis0.motor.config.current_lim =65
print("my_drive.axis0.motor.config.current_lim =100")
my_drive.axis0.motor.config.direction = 1   
print("my_drive.axis0.motor.config.direction = 1 ")
my_drive.axis0.motor.config.torque_constant = torque_constant
print("my_drive.axis0.motor.config.torque_constant =  " + str(torque_constant))
my_drive.axis0.sensorless_estimator.config.pm_flux_linkage = pm_flux_linkage
print("my_drive.axis0.sensorless_estimator.config.pm_flux_linkage = " + str(pm_flux_linkage))
my_drive.axis0.motor.config.phase_resistance = phase_resistance
print("my_drive.axis0.motor.config.phase_resistance = " + str(phase_resistance))
my_drive.axis0.motor.config.phase_inductance = phase_inductance
print("my_drive.axis0.motor.config.phase_inductance = " + str(phase_inductance))
my_drive.axis0.motor.config.pre_calibrated = True
print("my_drive.axis0.motor.config.pre_calibrated = True")
my_drive.axis0.motor.config.pole_pairs = pole_pairs
print("my_drive.axis0.motor.config.pole_pairs = " + str(pole_pairs))
my_drive.axis0.motor.config.gear_ratio = gear_ratio
print("my_drive.axis0.motor.config.gear_ratio = " + str(gear_ratio))

my_drive.axis0.encoder.config.bandwidth = 4000
print("my_drive.axis0.encoder.config.bandwidth = 4000")

my_drive.axis0.motor.config.current_lim = 65
print("my_drive.axis0.motor.config.current_lim = 65")

my_drive.axis0.motor.config.torque_lim = 65
print("my_drive.axis0.motor.config.torque_lim = 65")

my_drive.save_configuration()
print("my_drive.save_configuration()")
time.sleep(3)
# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

time.sleep(0.2)
