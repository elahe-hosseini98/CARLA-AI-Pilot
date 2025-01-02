from controller import Robot, Camera
from epuck_utils import (start_engine, enable_camera,
                         enable_customized_distance_sensors,
                         get_customized_distance_sensors_values,
                         get_image_from_camera, stop_engine
                         )
from velocity_adjustment import update_velocity_based_on_path
from data_pipeline.data_collection.create_excel import add_timestep_details_2_excel
import numpy as np


def check_maze_solved(robot: Robot, camera: Camera, redness_threshold=40):
    image = get_image_from_camera(camera)

    average_values = [np.mean(image[:, :, channel]) for channel in range(3)]

    if average_values[0] < redness_threshold:
        stop_engine(robot)
        return True

    return False


if __name__ == '__main__':
    micro_mouse = Robot()

    MAX_SPEED = 6.28

    timestep = int(micro_mouse.getBasicTimeStep())

    left_motor, right_motor = start_engine(micro_mouse, MAX_SPEED)
    camera = enable_camera(micro_mouse, timestep)
    dist_sensors = enable_customized_distance_sensors(micro_mouse, timestep)

    while micro_mouse.step(timestep) != -1:
        dist_sensor_values = get_customized_distance_sensors_values(dist_sensors)

        update_velocity_based_on_path(
            micro_mouse,dist_sensor_values, timestep, MAX_SPEED
        )

        if check_maze_solved(micro_mouse, camera):
            print("Congrats! You solved the maze!")
            break
