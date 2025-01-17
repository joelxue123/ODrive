import signal
import time
import logging
import statistics
import sys
import os
import subprocess

# 配置日志
logging.basicConfig(filename='signal_timer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

counter = 0
elapsed_times = []
target_interval = 0.001  # 1ms 目标间隔
num_measurements = 1000 # 测量次数

def handler(signum, frame):
    global counter, elapsed_times
    start_time = time.perf_counter()
    counter += 1
    logging.info(f"Signal received at {start_time}, Counter: {counter}")
    if counter >= num_measurements:
        signal.setitimer(signal.ITIMER_REAL, 0, 0) # 取消定时器
        return
    end_time = time.perf_counter()
    elapsed_times.append(end_time - start_time)


logging.info(f"System platform: {sys.platform}")
logging.info(f"Kernel version: {os.popen('uname -r').read().strip()}")

# 检查 POSIX 定时器是否启用
config_output = subprocess.check_output(['grep', 'CONFIG_POSIX_TIMERS', '/boot/config-' + os.popen('uname -r').read().strip()]).decode().strip()
if "CONFIG_POSIX_TIMERS=y" in config_output:
    logging.info("POSIX timers are enabled in the kernel.")
else:
    logging.error("POSIX timers are NOT enabled in the kernel.")
    logging.error("Please check your kernel configuration.")
    sys.exit(1)

signal.signal(signal.ITIMER_REAL, handler)
signal.setitimer(signal.ITIMER_REAL, target_interval, target_interval)  # 1ms 定时

while counter < num_measurements:
    time.sleep(0.0001) # 主线程休眠，避免占用过多CPU

logging.info(f"Average signal interval: {statistics.mean(elapsed_times)}, std dev: {statistics.stdev(elapsed_times) if len(elapsed_times) > 1 else 0}")
logging.info("Main thread finished.")
