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

def find_cross_indices(encodervalue_data):
    """Find indices where encoder value wraps around (crosses 32768 threshold)
    Args:
        encodervalue_data: List of encoder values (0-65535)
    Returns:
        List of indices where wraparound occurs
    """
    if len(encodervalue_data) < 2:
        return []
        
    cross_points = []
    for i in range(1, len(encodervalue_data)):
        # Check for wraparound (jump larger than half the range)
        if abs(encodervalue_data[i] - encodervalue_data[i-1]) > 32768:
            cross_points.append(i)
            
    return cross_points


def store_phase_error_period(data):

    # Save to file
    with open('phase_error_compensation.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Index', 'Phase_Error'])
        for i, error in enumerate(data):
            writer.writerow([i, error])
            
    logging.info(f"Saved {len(data)} phase error points for compensation")
    return data


def load_phase_error_compensation(filename='phase_error_compensation.csv'):
    """Load phase error compensation data from CSV
    Args:
        filename: CSV file path containing phase error data
    Returns:
        List of phase error values
    """
    try:
        phase_error_data = []
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                phase_error_data.append(float(row['Phase_Error']))
                
        logging.info(f"Loaded {len(phase_error_data)} phase error points from {filename}")
        return phase_error_data
        
    except FileNotFoundError:
        logging.error(f"Compensation file {filename} not found")
        return None
    except Exception as e:
        logging.error(f"Error loading compensation data: {e}")
        return None

def get_period_data(first_crossing, second_crossing, data):
    """Extract one period of data between crossings
    Args:
        first_crossing: Index of first crossing point
        second_crossing: Index of second crossing point
        data: List of data to extract period from
    Returns:
        List containing one period of data between crossings
    """
    # Validate inputs
    if first_crossing >= second_crossing:
        logging.error("Invalid crossing points: first must be less than second")
        return None
        
    if first_crossing < 0 or second_crossing > len(data):
        logging.error("Crossing points out of data range")
        return None
    # Get one period
    start_idx = first_crossing
    end_idx = second_crossing
    period_data = data[start_idx:end_idx]
    
    logging.info(f"Extracted period with {len(period_data)} points")
    return period_data

if __name__ == '__main__':

    print("finding an odrive...")
    my_drive = odrive.find_any()
    can_id = my_drive.axis0.config.can_node_id
    logging.info(f"can_id: {can_id}")
    my_drive.axis0.requested_state = AXIS_STATE_IDLE
    time.sleep(0.1)
    my_drive.axis0.clear_errors()
    my_drive.axis0.motor.using_old_torque_constant = True
    my_drive.axis0.config.enable_watchdog = False
    my_drive.axis0.encoder.config.is_high_speed_encode_query_enabled = True
    my_drive.axis0.clear_errors()
    time.sleep(0.1)
    my_drive.axis0.config.general_lockin.current = 5
    my_drive.axis0.config.general_lockin.vel = 20
    my_drive.axis0.clear_errors()

    my_drive.axis0.requested_state = AXIS_STATE_LOCKIN_SPIN
    time.sleep(2)
    phase_data = []
    encodervalue_data = []
    phase_error_data = []
    samples = []
    for i in range(1400):
        phase_encodervalue_packed = my_drive.axis0.phase_encodervalue_packed
        phase = (phase_encodervalue_packed>>16)& 0x0000FFFF
        phase = 65535 - phase
        encodervalue = phase_encodervalue_packed & 0x0000FFFF
        logging.info(f"phase: {phase}, encodervalue: {encodervalue}")
        phase_data.append(phase)
        encodervalue_data.append(encodervalue)
        samples.append(i)
        
        time.sleep(0.01)

    cross_points = find_cross_indices(encodervalue_data)
    logging.info(f"Cross points: {cross_points}")
    idex = cross_points[0]
    logging.info(f"Cross index: {idex}")
    logging.info(f"Cross data: {encodervalue_data[idex]}")

    offset = encodervalue_data[idex] - phase_data[idex]
    phase_data = [x + offset for x in phase_data]
    phase_data = [x % 65536 for x in phase_data]
    phase_error_data = [x - encodervalue_data[i] for i, x in enumerate(phase_data)]
    

    phase_error_data = get_period_data(cross_points[0], cross_points[1], phase_error_data)
    phase_data = get_period_data(cross_points[0], cross_points[1], phase_data)
    encodervalue_data = get_period_data(cross_points[0], cross_points[1], encodervalue_data)
    phase_error_compensation =  load_phase_error_compensation('phase_error_compensation.csv')
    encodervalue_data = [x + phase_error_compensation[i] for i, x in enumerate(encodervalue_data)]
    phase_error_data = [x - encodervalue_data[i] for i, x in enumerate(phase_data)]
    samples = [i for i in range(len(phase_data))]
    #store_phase_error_period(phase_error_data)

    my_drive.axis0.requested_state = AXIS_STATE_IDLE


   # Plot data
    plt.figure(figsize=(12,6))
    plt.plot(samples, phase_data, 'b-', label='Phase')
    plt.plot(samples, encodervalue_data, 'r-', label='Encoder Value')
    plt.plot(samples, phase_error_data, 'g-', label='Phase Error')
    plt.xlabel('Sample Number')
    plt.ylabel('Value')
    plt.title('Phase and Encoder Values vs Sample Number')
    plt.legend()
    plt.grid(True)
    plt.show()

