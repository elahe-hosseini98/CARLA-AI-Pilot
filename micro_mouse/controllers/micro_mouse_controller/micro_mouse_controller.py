from controller import Robot
from epuck_utils import (start_engine, enable_camera,
                         enable_customized_distance_sensors,
                         get_customized_distance_sensors_values
                         )
from velocity_adjustment import update_velocity_based_on_path


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