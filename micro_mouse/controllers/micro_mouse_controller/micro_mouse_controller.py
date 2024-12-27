from controller import Robot
from epuck_utils import start_engine, enable_sensors, enable_camera, get_ir_sensors_values
from velocity_adjustment import update_velocity_based_on_path
import numpy as np
import cv2


if __name__ == '__main__':
    micro_mouse = Robot()

    MAX_SPEED = 6.28

    timestep = int(micro_mouse.getBasicTimeStep())

    left_motor, right_motor = start_engine(micro_mouse, MAX_SPEED)
    camera = enable_camera(micro_mouse, timestep)
    ir_sensors = enable_sensors(micro_mouse, timestep)

    while micro_mouse.step(timestep) != -1:
        ir_sensor_values = get_ir_sensors_values(ir_sensors)
        print(ir_sensor_values)

        update_velocity_based_on_path(
            micro_mouse,ir_sensor_values, timestep, MAX_SPEED
        )
