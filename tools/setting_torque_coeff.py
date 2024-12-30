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


positive_torque_coeff = [1.1775, 1.1775, 1.1775, 1.1775, 1.1775, 1.1775, 1.1775, 1.1775, 1.1775, 1.1775, 1.1775, 1.1775, 1.1813, 1.1863, 1.1888, 1.1949, 1.1977, 1.183, 1.1748, 1.1766, 1.1877, 1.1987, 1.1935, 1.1872, 1.1891, 1.1942, 1.2016, 1.2081, 1.2092, 1.2035, 1.1944, 1.1855, 1.1794, 1.174, 1.172, 1.1694, 1.1664, 1.1607, 1.1534, 1.1447, 1.1362, 1.129, 1.1232, 1.1174, 1.1131, 1.1102, 1.108, 1.1048, 1.1014, 1.0983, 1.096, 1.0939, 1.0908, 1.0871, 1.0819, 1.0749, 1.0674, 1.0595, 1.0499, 1.0367]

negative_torque_coeff = [1.2362, 1.2362, 1.2362, 1.2362, 1.2362, 1.2362, 1.2362, 1.2362, 1.2362, 1.2362, 1.2362, 1.2362, 1.2458, 1.2533, 1.257, 1.2564, 1.2543, 1.2507, 1.2484, 1.2476, 1.2471, 1.2333, 1.2177, 1.2123, 1.2108, 1.2142, 1.2181, 1.215, 1.2078, 1.2053, 1.2058, 1.2085, 1.2135, 1.2195, 1.2218, 1.2192, 1.2137, 1.2079, 1.2031, 1.201, 1.2014, 1.2022, 1.2024, 1.2027, 1.2005, 1.1949, 1.1871, 1.1799, 1.1732, 1.168, 1.1614, 1.1551, 1.1499, 1.1465, 1.1448, 1.1442, 1.1409, 1.1339, 1.1232, 1.1135]




#positive_torque_coeff = [2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5]
#negative_torque_coeff = [2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5]

current2torque_coeff_p_ = [1.1864, 1.1864, 1.1864, 1.1864, 1.1864, 1.1864, 1.1864, 1.1864, 1.1864, 1.1864, 1.1864, 1.1864, 1.1916, 1.1978, 1.1871, 1.1755, 1.1766, 1.1946, 1.1964, 1.1876, 1.189, 1.1966, 1.2068, 1.2092, 1.2031, 1.1938, 1.1854, 1.1793, 1.1739, 1.1716, 1.1688, 1.165, 1.1592, 1.1519, 1.1443, 1.1368, 1.1301, 1.1248, 1.1192, 1.1147, 1.1117, 1.1087, 1.1063, 1.1031, 1.0999, 1.097, 1.0949, 1.0929, 1.0897, 1.0856, 1.0811, 1.0755, 1.0696, 1.0641, 1.058, 1.0515, 1.0438, 1.0357, 1.0276,1.0276]
current2torque_coeff_n_ = [1.2569, 1.2569, 1.2569, 1.2569, 1.2569, 1.2569, 1.2569, 1.2569, 1.2569, 1.2569, 1.2569, 1.2569, 1.2561, 1.2521, 1.2494, 1.2475, 1.2457, 1.2304, 1.2167, 1.2116, 1.2119, 1.2176, 1.2153, 1.2079, 1.2051, 1.2065, 1.2117, 1.2204, 1.221, 1.2169, 1.2105, 1.2048, 1.2015, 1.2012, 1.2021, 1.2025, 1.2021, 1.1981, 1.1915, 1.1839, 1.1781, 1.1719, 1.167, 1.1609, 1.1552, 1.1503, 1.1467, 1.1449, 1.1439, 1.1408, 1.135, 1.1273, 1.1195, 1.1127, 1.1051, 1.0965, 1.0876, 1.079, 1.0714,1.0714]





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