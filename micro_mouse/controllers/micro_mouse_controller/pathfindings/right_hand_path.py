def navigate_with_ir(ir_sensor_values):
    if ir_sensor_values[0] < 10:
        return 1
    return 0