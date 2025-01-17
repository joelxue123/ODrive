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
import matplotlib.pyplot as plt
import threading
# Find a connected ODrive (this will block until you connect one)



print("finding an odrive...")
my_drive = odrive.find_any()
time.sleep(1)


axis_error = my_drive.axis0.error
motor_error = my_drive.axis0.motor.error
encoder_error = my_drive.axis0.encoder.error

print("axis error: ", axis_error)
print("motor error: ", motor_error)
print("encoder error: ", encoder_error)

motor_test_failed  = motor_error + encoder_error

kp_gain = my_drive.axis0.kp_gain
kd_gain = my_drive.axis0.kd_gain

if kp_gain != 1 or kd_gain != 1:
    print("kp_gain or kd_gain is not 1")
    exit()

if motor_test_failed == 0:
    print("motor test passed")
    my_drive.axis0.config.enable_watchdog = False
    my_drive.axis0.clear_errors()
    time.sleep(0.1)
    my_drive.axis0.motor.using_old_torque_constant = False
    my_drive.axis0.controller.input_torque = 0
    my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
else:
    print("motor test failed")
    exit()

current_data = []
my_drive.axis0.motor.config.current_control_bandwidth= 5000


torque_sign = 1
data_count = 0
torque_sign = 1
data_count = 0
lock = threading.Lock()

def collect_data():
    global current_data, torque_sign, data_count
    with lock:
        try:
            current_data.append(my_drive.axis0.motor.current_control.Iq_measured)
            data_count += 1
            if  data_count>= 2000:
                my_drive.axis0.requested_state = AXIS_STATE_IDLE
                return True
            return False
        except Exception as e:
            print(f"Error in collect_ {e}")
            return True
            

def send_data():
    global current_data, torque_sign, data_count
    data_count += 1
    my_drive.axis0.controller.input_torque = torque_sign * 8
    torque_sign = -1 * torque_sign

def run_timed_loop():
    global current_data, torque_sign, data_count
    print(time.perf_counter())
    interval = 0.002  # 1ms interval
    timer = threading.Timer(interval, run_timed_loop)
    timer.start()
    if data_count % 10 == 0:
        send_data()
    else:
        if collect_data():
            timer.cancel()

      

print(time.time())
run_timed_loop()
print(time.time())

time.sleep(10)
my_drive.axis0.requested_state = AXIS_STATE_IDLE
plt.figure(figsize=(10, 6))  # Adjust figure size as needed
plt.plot(current_data)
plt.xlabel("Sample Number")
plt.ylabel("Current (Amps)")  # Adjust units as needed
plt.title("ODrive Current Data")
plt.grid(True)
plt.show()

