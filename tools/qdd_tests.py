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

class QDDError(Enum):
    QDD_ERROR_NONE = 0
    QDD_ERROR_CAN_LOST = 2048
    QDD_ERROR_TIMEOUT = 2049
    QDD_ERROR_INVALID_ARG = 2050
    QDD_ERROR_GENERAL = 2051


TORQUE_VELOCITY_THRESHOLD = 20


def qdd_test(my_drive):
    my_drive.axis0.clear_errors()
    my_drive.axis0.controller.config.kp = 0
    my_drive.axis0.controller.config.kd = 0
    axis_error = my_drive.axis0.error
    motor_error = my_drive.axis0.motor.error
    encoder_error = my_drive.axis0.encoder.error
    
    logging.info(f"Axis error: {axis_error}")
    logging.info(f"Motor error: {motor_error}")
    logging.info(f"Encoder error: {encoder_error}")

    if axis_error != QDDError.QDD_ERROR_CAN_LOST.value:
        logging.warning("Axis error is not can_lost_error")

    voltage = my_drive.vbus_voltage
    logging.info(f"Voltage: {voltage}")

    motor_test_failed  = motor_error + encoder_error

    kp_gain = my_drive.axis0.kp_gain
    kd_gain = my_drive.axis0.kd_gain

    if kp_gain != 1 or kd_gain != 1:
        logging.error("kp_gain or kd_gain is not 1")
        return False

    if motor_test_failed == 0:
        logging.info("kp_gain and kd_gain are 1, test passed")

    else:
        
        logging.error("Motor test failed")
        return False
    
    logging.info("qdd_test passed")
    return True

def qdd_lockin_test(my_drive):
    my_drive.axis0.motor.using_old_torque_constant = True
    my_drive.axis0.config.enable_watchdog = False
    my_drive.axis0.encoder.config.is_high_speed_encode_query_enabled = True
    my_drive.axis0.config.general_lockin.current = 5
    my_drive.axis0.config.general_lockin.vel = 20
    my_drive.axis0.clear_errors()
    time.sleep(0.1)
    initial_motor_pos = my_drive.axis0.encoder.pos_abs/2**16
    initial_gear_pos = my_drive.axis0.encoder.sencond_pos_abs/2**18
    initial_gear_boxpos_rad = my_drive.axis0.encoder.gear_boxpos_rad
    


    my_drive.axis0.requested_state = AXIS_STATE_LOCKIN_SPIN
    time.sleep(5)
    my_drive.axis0.requested_state = AXIS_STATE_IDLE
    final_motor_pos = my_drive.axis0.encoder.pos_abs/2**16
    final_gear_pos = my_drive.axis0.encoder.sencond_pos_abs/2**18


    motor_pos_walk_distance =final_motor_pos - initial_motor_pos
    if motor_pos_walk_distance < 0:
        motor_pos_walk_distance += 1

    gear_pos_walk_distance = final_gear_pos - initial_gear_pos
    if gear_pos_walk_distance < 0:
        gear_pos_walk_distance += 1

    
    logging.info(f"Initial motor pos: {initial_motor_pos}")
    logging.info(f"Final motor pos: {final_motor_pos}")
    logging.info(f"Initial gear box pos (rad): {initial_gear_boxpos_rad}")
    logging.info(f"Initial gear pos: {initial_gear_pos}")
    logging.info(f"Final gear pos: {final_gear_pos}")
    logging.info(f"motor_pos_walk_distance: {motor_pos_walk_distance}")
    logging.info(f"gear_pos_walk_distance: {gear_pos_walk_distance}")

    if (motor_pos_walk_distance) < 0.5: # 0.5 is 经验值
        logging.error("Motor position test failed")
        return False
    if (gear_pos_walk_distance) < 0.5/16: #16是减速比
        logging.error("Gear position test failed")
        return False
    else:
        logging.info("Motor position test passed")
        logging.info("Gear position test passed")
        logging.info("qdd_lockin_test passed")
        return True


def qdd_torque_test(my_drive):
    my_drive.axis0.config.enable_watchdog = False
    my_drive.axis0.clear_errors()
    time.sleep(0.1)
    my_drive.axis0.motor.using_old_torque_constant = False
    my_drive.axis0.controller.input_torque = 1
    my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    time.sleep(5)
    
    velocity = my_drive.axis0.encoder.vel_estimate
    my_drive.axis0.requested_state = AXIS_STATE_IDLE

    logging.info(f"Velocity: {velocity}")
    if velocity < TORQUE_VELOCITY_THRESHOLD:
        logging.error("Torque test failed")
        return False
    else:
        logging.info("Torque test passed")

    
    logging.info("qdd_torque_test passed")
    return True


def qdd_mu_sensor_test(my_drive):
    my_drive.axis0.motor.using_old_torque_constant = True
    my_drive.axis0.config.enable_watchdog = False
    my_drive.axis0.config.general_lockin.current = 10
    my_drive.axis0.config.general_lockin.vel = 150
    my_drive.axis0.clear_errors()
    my_drive.axis0.requested_state = AXIS_STATE_IDLE
    time.sleep(0.1)

    current_state = my_drive.axis0.current_state
    logging.info(f"Current state: {current_state}")
    stauts =  my_drive.axis0.encoder.start_encoder_test_thread()
    time.sleep(0.1)
    my_drive.axis0.requested_state = AXIS_STATE_LOCKIN_SPIN
    time.sleep(1)
    axis_error = my_drive.axis0.error
    motor_error = my_drive.axis0.motor.error
    encoder_error = my_drive.axis0.encoder.error
    
    logging.info(f"Axis error: {axis_error}")
    logging.info(f"Motor error: {motor_error}")
    logging.info(f"Encoder error: {encoder_error}")

    if stauts == False:
        logging.error("Start encoder test thread failed")
    
    my_drive.axis0.encoder.signal_encoder_thread()
    time.sleep(0.004)

    motor_encoder_errors = 0
    gear_encoder_errors = 0
    for i in range(5000):

        motor_mu150_status = my_drive.axis0.encoder.motor_mu150_status
        gear_mu150_status = my_drive.axis0.encoder.gear_mu150_status
        if motor_mu150_status == 0:
            logging.info("motor_mu150_status test passed")
        else:
            logging.error("motor_mu150_status test failed")
            logging.error(motor_mu150_status)
            logging.error(gear_mu150_status)
            motor_encoder_errors += 1
            
            

        if gear_mu150_status == 0:
            logging.info("gear_mu150_status test passed")
            
        else:
            logging.error("gear_mu150_status test failed")
            logging.error(motor_mu150_status)
            logging.error(gear_mu150_status)
            gear_encoder_errors += 1
            
            
        status  = my_drive.axis0.encoder.signal_encoder_thread()
        if status == False:
            logging.error("signal encoder thread failed")
            
        time.sleep(0.005)

    logging.info(f"motor_encoder_errors: {motor_encoder_errors}")
    logging.info(f"gear_encoder_errors: {gear_encoder_errors}")
    time.sleep(0.1)
    my_drive.axis0.encoder.stop_encoder_test_thread()
    time.sleep(0.1)
    my_drive.axis0.requested_state = AXIS_STATE_IDLE




if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_option = sys.argv[1]
        if test_option != "all":
            print("invalid test option")
            exit()
    else:
        test_option = "only lockin"

    print("finding an odrive...")
    my_drive = odrive.find_any()
    can_id = my_drive.axis0.config.can_node_id
    logging.info(f"can_id: {can_id}")
    time.sleep(1)
    qdd_test_passed = qdd_test(my_drive)
    if my_drive:
        if qdd_test_passed:

            #qdd_mu_sensor_test(my_drive)
            qdd_lockin_test(my_drive)
            if test_option == "all":
                qdd_torque_test(my_drive)
                pass
            else:
                pass

        else:
            print("qdd test failed")
    else:
        print("no odrive found")

