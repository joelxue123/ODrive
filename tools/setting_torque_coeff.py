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
# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()
time.sleep(1)

torque_cof = my_drive.axis0.motor.config.torque_constant
print("torque_cof is " + str(torque_cof))

""" for item in range(0,20):
    torque = 55
    my_drive.axis0.motor.setting_motor_torque_linearity(item, torque)
    print("setting torque_cof is " + str(torque) )
    time.sleep(0.001) """

""" for item in range(0,20):
    torque = my_drive.axis0.motor.get_motor_torque_linearity(item)
    print("getting torque_cof is " + str(torque) )
    time.sleep(0.001) """
   
""" for item in range(0,20):
    current = 66
    my_drive.axis0.motor.setting_motor_current_linearity(item, current)
    print("setting current is " + str(current) )
    time.sleep(0.001) """

""" for item in range(0,20):
    current = my_drive.axis0.motor.get_motor_current_linearity(item)
    print("getting torque_cof is " + str(current) )
    time.sleep(0.001) """



positive_torque_coeff = [1.2721, 1.2721, 1.2721, 1.2721, 1.2721, 1.2721, 1.2721, 1.2721, 1.2721, 1.2721, 1.2721, 1.2784, 1.2856, 1.2902, 1.2924, 1.2915, 1.2918, 1.2928, 1.2927, 1.292, 1.2896, 1.2845, 1.2773, 1.269, 1.2599, 1.2513, 1.2403, 1.2317, 1.225, 1.2187, 1.2115, 1.2053, 1.1989, 1.1935, 1.188, 1.1814, 1.1773, 1.1741, 1.1684, 1.1648, 1.1608, 1.156, 1.1515, 1.1469, 1.1423, 1.1367, 1.1337, 1.135, 1.1394, 1.1456, 1.1515, 1.1566, 1.1622, 1.1678, 1.1715, 1.1727, 1.169, 1.1639, 1.1573, 1.1491]
negative_torque_coeff = [1.1846, 1.1846, 1.1846, 1.1846, 1.1846, 1.1846, 1.1846, 1.1846, 1.1846, 1.1846, 1.1846, 1.1846, 1.1932, 1.1958, 1.1982, 1.2039, 1.2075, 1.2096, 1.2132, 1.2176, 1.224, 1.2288, 1.2324, 1.2359, 1.2397, 1.2413, 1.2416, 1.2425, 1.2419, 1.2416, 1.2402, 1.2398, 1.2414, 1.2429, 1.2435, 1.2441, 1.2449, 1.2462, 1.246, 1.2461, 1.2464, 1.245, 1.2436, 1.242, 1.2392, 1.2364, 1.2329, 1.2284, 1.223, 1.2151, 1.1933, 1.1671, 1.1402, 1.1196, 1.1047, 1.0937, 1.0771, 1.0597, 1.0382, 1.0165]
#positive_torque_coeff = [2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5]
#negative_torque_coeff = [2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5]


current2torque_coeff_p_ = [1.2923, 1.2923, 1.2923, 1.2923, 1.2923, 1.2923, 1.2923, 1.2923, 1.2923, 1.2923, 1.2923, 1.2923, 1.291, 1.2922, 1.2923, 1.2908, 1.2856, 1.2774, 1.2683, 1.2587, 1.2486, 1.238, 1.2298, 1.2227, 1.215, 1.2085, 1.2026, 1.1964, 1.1907, 1.184, 1.1787, 1.1756, 1.1703, 1.1654, 1.1622, 1.1579, 1.1529, 1.1484, 1.1441, 1.1392, 1.1346, 1.1341, 1.1393, 1.1492, 1.1571, 1.1656, 1.1715, 1.1724, 1.168, 1.1632, 1.1573, 1.1505, 1.1431, 1.135, 1.1264, 1.1174, 1.1076, 1.0987, 1.0903,1.0903]
current2torque_coeff_n_ = [1.197, 1.197, 1.197, 1.197, 1.197, 1.197, 1.197, 1.197, 1.197, 1.197, 1.197, 1.197, 1.2022, 1.2074, 1.2097, 1.2148, 1.2224, 1.2292, 1.2339, 1.2385, 1.2418, 1.2416, 1.2417, 1.2411, 1.2402, 1.2402, 1.2424, 1.2432, 1.2442, 1.2458, 1.2459, 1.246, 1.2463, 1.2445, 1.243, 1.2405, 1.2371, 1.2333, 1.2288, 1.2233, 1.2165, 1.2038, 1.1903, 1.1761, 1.1604, 1.1469, 1.1327, 1.1215, 1.1112, 1.1032, 1.0957, 1.0858, 1.0764, 1.0672, 1.0567, 1.0464, 1.0365, 1.0261, 1.0167,1.0167]

for item in range(0,60):
    current  =positive_torque_coeff[item]
    my_drive.axis0.motor.setting_positive_torque_slope(item, current)
    print("setting positive torque_slope is " +str(item) +":" + str(current) )
    time.sleep(0.001)

for item in range(0,60):
    current = my_drive.axis0.motor.get_positive_torque_slope(item)
    print("getting positive torque_slope is " + str(current) )
    time.sleep(0.001)


for item in range(0,60):
    current  =negative_torque_coeff[item]
    my_drive.axis0.motor.setting_negative_torque_slope(item, current)
    print("setting negative torque_slope is " +str(item) +":" + str(current) )
    time.sleep(0.001)

for item in range(0,60):
    current = my_drive.axis0.motor.get_negative_torque_slope(item)
    print("getting negative torque_slope is " + str(current) )
    time.sleep(0.001)


for item in range(0,60):
    current2torque_coeff_p  =current2torque_coeff_p_[item]
    my_drive.axis0.motor.setting_current2torque_slope(2*item, current2torque_coeff_p)
    print("setting pos current 2 torque_slope is " +str(2*item) +":" + str(current2torque_coeff_p) )
    time.sleep(0.001)
    current2torque_coeff_n  =current2torque_coeff_n_[item]
    my_drive.axis0.motor.setting_current2torque_slope(2*item+1, current2torque_coeff_n)
    print("setting neg current 2 torque_slope is " +str(2*item+1) +":" + str(current2torque_coeff_n) )
    time.sleep(0.001)

for item in range(0,60):
    current2torque_coeff_p  =  my_drive.axis0.motor.getting_current2torque_slope(2*item)
    print("getting pos current 2 torque_slope is " +str(2* item) +":" + str(current2torque_coeff_p) )
    time.sleep(0.001)
    current2torque_coeff_n  = my_drive.axis0.motor.getting_current2torque_slope(2*item+1)
    print("getting neg current 2 torque_slope is " +str(2*item+1) +":" + str(current2torque_coeff_n) )
    time.sleep(0.001)




my_drive.axis0.controller.input_torque = 0

# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

my_drive.save_configuration()
print("my_drive.save_configuration()")

time.sleep(1)

plt.show()