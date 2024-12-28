from controller import Robot, Camera
from epuck_utils import (start_engine, enable_camera,
                         enable_customized_distance_sensors,
                         get_customized_distance_sensors_values,
                         get_image_from_camera, stop_engine
                         )
from velocity_adjustment import update_velocity_based_on_path
import numpy as np


def check_maze_solved(robot: Robot, camera: Camera):
    image = get_image_from_camera(camera)

    total_pixels = image.shape[0] * image.shape[1]

    # Count the number of red-ish pixels (Red > Green and Blue)
    redish_pixels = np.sum(image[:, :, 0] > (image[:, :, 1] + image[:, :, 2]))

    # Calculate the ratio of red-ish pixels
    red_ratio = redish_pixels / total_pixels

    print('red_ratio =', red_ratio)

    if red_ratio > 0.9:
        stop_engine(robot)
        return True # Return True if more than 50% of the image is red-ish

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

        print(dist_sensor_values)

        update_velocity_based_on_path(
            micro_mouse,dist_sensor_values, timestep, MAX_SPEED
        )

        if check_maze_solved(micro_mouse, camera):
            print("Congrats! You solved the maze!")
            break