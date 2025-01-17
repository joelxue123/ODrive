
commands = []
commands.append("save_flash.py")
commands.append("qdd_tests.py")
commands.append("run_offset_calibration.py")
commands.append("odrive_save_sensor_param.py")
commands.append("calibration_ic_huas_encoder.py")
commands.append("setting_torque_coeff.py")
commands.append("change_canid.py")
commands.append("read_motor_status.py")


print("commands lists:")
for command in commands:
    print(command)