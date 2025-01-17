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


#positive_torque_coeff = [1.174,1.174,1.174,1.174,1.174,1.174,1.174,1.174,1.174,1.174,1.174,1.174,1.1804,1.1852,1.1926,1.1995,1.2061,1.2105,1.2139,1.2158,1.2158,1.2138,1.2099,1.2047,1.1967,1.1909,1.1886,1.1898,1.1941,1.1981,1.1944,1.1858,1.1843,1.1877,1.1933,1.2005,1.2016,1.1829,1.1573,1.1476,1.1468,1.1481,1.1463,1.1436,1.145,1.1427,1.1369,1.131,1.1217,1.1163,1.1174,1.1181,1.1179,1.1059,1.0418,1.0311,1.0307,1.0344,1.0361,1.0364]

#negative_torque_coeff = [1.2735,1.2735,1.2735,1.2735,1.2735,1.2735,1.2735,1.2735,1.2735,1.2735,1.2735,1.2735,1.2758,1.2747,1.2719,1.2711,1.2669,1.2634,1.2591,1.2526,1.2486,1.2454,1.2405,1.2349,1.2289,1.2243,1.2196,1.2147,1.2096,1.2062,1.2087,1.2135,1.2208,1.2294,1.2331,1.2244,1.2107,1.2073,1.2095,1.2133,1.2091,1.1948,1.1797,1.1653,1.161,1.1547,1.1506,1.1512,1.1539,1.1576,1.1609,1.1484,1.1277,1.1086,1.1053,1.1085,1.1126,1.1124,1.1046,1.0476]

positive_torque_coeff = [1.1921, 1.1921, 1.1921, 1.1921, 1.1921, 1.1921, 1.1921, 1.1921, 1.1921, 1.1921, 1.1921, 1.1921, 1.1922, 1.1935, 1.1946, 1.1971, 1.198, 1.1965, 1.1916, 1.1859, 1.181, 1.1734, 1.1672, 1.1627, 1.157, 1.1537, 1.1522, 1.1507, 1.1501, 1.1508, 1.1517, 1.1527, 1.1544, 1.156, 1.1579, 1.1606, 1.1628, 1.1656, 1.1677, 1.1702, 1.1719, 1.1734, 1.1743, 1.1748, 1.1756, 1.1755, 1.1754, 1.1759, 1.1764, 1.177, 1.1783, 1.1794, 1.1796, 1.1794, 1.1792, 1.1803, 1.1733, 1.1424, 1.108, 1.0727]
negative_torque_coeff = [1.276, 1.276, 1.276, 1.276, 1.276, 1.276, 1.276, 1.276, 1.276, 1.276, 1.276, 1.276, 1.2731, 1.2681, 1.2618, 1.2542, 1.2461, 1.2381, 1.2308, 1.2242, 1.2188, 1.2146, 1.2114, 1.209, 1.2072, 1.2061, 1.2052, 1.2047, 1.2042, 1.2038, 1.2031, 1.2027, 1.2022, 1.2016, 1.2011, 1.2007, 1.2008, 1.2011, 1.2018, 1.2028, 1.204, 1.2056, 1.2073, 1.2091, 1.211, 1.2128, 1.2146, 1.2163, 1.2181, 1.22, 1.2212, 1.2213, 1.2198, 1.2161, 1.2098, 1.2008, 1.1877, 1.1711, 1.1529, 1.1336]
#positive_torque_coeff = [2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5]
#negative_torque_coeff = [2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5]

#current2torque_coeff_p_ = [1.1872,1.1872,1.1872,1.1872,1.1872,1.1872,1.1872,1.1872,1.1872,1.1872,1.1872,1.1872,1.1964,1.2052,1.2112,1.2148,1.2162,1.2144,1.211,1.2041,1.1956,1.1903,1.1884,1.1919,1.1981,1.1939,1.1858,1.1847,1.1905,1.2005,1.1999,1.1853,1.1678,1.1536,1.1472,1.1469,1.1482,1.1443,1.1446,1.1436,1.1391,1.1334,1.1273,1.1192,1.1164,1.1176,1.1182,1.1156,1.1033,1.0855,1.0672,1.0514,1.0398,1.0325,1.031,1.0341,1.0361,1.0362,1.0262,1.0262]
#current2torque_coeff_n_ = [1.2723,1.2723,1.2723,1.2723,1.2723,1.2723,1.2723,1.2723,1.2723,1.2723,1.2723,1.2723,1.2687,1.2642,1.2594,1.2524,1.2479,1.2433,1.2381,1.2309,1.2255,1.2205,1.2149,1.2095,1.2063,1.2108,1.2204,1.2327,1.2292,1.2165,1.2081,1.2082,1.2133,1.2083,1.1968,1.1849,1.1729,1.1639,1.1591,1.1538,1.1504,1.1523,1.1562,1.1609,1.1521,1.1393,1.1277,1.1157,1.1066,1.1058,1.1117,1.1127,1.1081,1.0979,1.0831,1.0666,1.0514,1.0379,1.0263,1.0263]

current2torque_coeff_p_ = [1.2586, 1.2586, 1.2586, 1.2586, 1.2586, 1.2586, 1.2586, 1.2586, 1.2586, 1.2586, 1.2586, 1.2586, 1.2528, 1.2474, 1.2407, 1.2357, 1.2291, 1.2237, 1.2191, 1.2161, 1.2118, 1.2064, 1.1996, 1.1924, 1.1837, 1.1744, 1.1659, 1.1587, 1.151, 1.146, 1.1394, 1.1341, 1.1289, 1.1256, 1.1233, 1.1219, 1.1222, 1.1226, 1.123, 1.1242, 1.1239, 1.1255, 1.1277, 1.1305, 1.1332, 1.1353, 1.1362, 1.135, 1.1345, 1.137, 1.1409, 1.1469, 1.1485, 1.1416, 1.1298, 1.1164, 1.1028, 1.0887, 1.0749, 1.0749]
current2torque_coeff_n_ = [1.3585, 1.3585, 1.3585, 1.3585, 1.3585, 1.3585, 1.3585, 1.3585, 1.3585, 1.3585, 1.3585, 1.3585, 1.3533, 1.3468, 1.3393, 1.3307, 1.3214, 1.311, 1.3001, 1.2891, 1.278, 1.2671, 1.2567, 1.247, 1.2381, 1.2301, 1.2229, 1.2165, 1.2109, 1.2061, 1.2021, 1.1985, 1.1954, 1.1925, 1.1899, 1.1873, 1.1848, 1.1822, 1.1796, 1.1769, 1.174, 1.1711, 1.1683, 1.1658, 1.1645, 1.1668, 1.1719, 1.1764, 1.1791, 1.18, 1.179, 1.176, 1.1692, 1.1591, 1.1485, 1.138, 1.1251, 1.1111, 1.0974, 1.0974]



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