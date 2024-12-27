from controller import Robot, Camera
import numpy as np
import cv2


def start_engine(robot: Robot, max_speed: float):
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')

    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    left_motor.setVelocity(max_speed)
    right_motor.setVelocity(max_speed)

    return left_motor, right_motor


def enable_sensors(robot: Robot, timestep: int):
    ps = []
    ps_names = ['ps' + str(i) for i in range(8)]

    for name in ps_names:
        sensor = robot.getDevice(name)
        sensor.enable(timestep)
        ps.append(sensor)

    return ps


def normalize_ps_values(sensor_values):
    return [1000/sensor_value if sensor_value != 0 else sensor_value for sensor_value in sensor_values]


def get_ir_sensors_values(ir_sensors):
    ir_sensor_values = [sensor.getValue() for sensor in ir_sensors]
    return normalize_ps_values(ir_sensor_values)


def enable_camera(robot: Robot, timestep: int):
    camera = robot.getDevice('camera')
    camera.enable(timestep)

    return camera


def display_camera(robot: Robot, camera: Camera, timestep: int):
    while robot.step(timestep) != -1:
        image_data = camera.getImage()

        width = camera.getWidth()
        height = camera.getHeight()

        image_array = np.frombuffer(image_data, dtype=np.uint8).reshape((height, width, 4))

        image_array = image_array[:, :, :3]

        cv2.imshow("e-puck Camera", image_array)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()