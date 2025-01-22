from controller import Robot, Keyboard
import numpy as np
import cv2
import pandas as pd
import os


def initialize_robot():
    robot = Robot()
    keyboard = Keyboard()
    timestep = int(robot.getBasicTimeStep())
    keyboard.enable(timestep)
    return robot, keyboard, timestep


def get_devices(robot):
    devices = {
        "left_steer": robot.getDevice("left_steer"),
        "right_steer": robot.getDevice("right_steer"),
        "engine_speaker": robot.getDevice("engine_speaker"),
        "left_front_wheel": robot.getDevice("left_front_wheel"),
        "right_front_wheel": robot.getDevice("right_front_wheel"),
        "left_front_brake": robot.getDevice("left_front_brake"),
        "right_front_brake": robot.getDevice("right_front_brake"),
        "camera": robot.getDevice("camera"),
    }
    return devices


def configure_wheels(left_front_wheel, right_front_wheel):
    left_front_wheel.setPosition(float('inf'))
    right_front_wheel.setPosition(float('inf'))
    left_front_wheel.setVelocity(0)
    right_front_wheel.setVelocity(0)


def configure_camera(camera, timestep):
    camera.enable(timestep)
    width = camera.getWidth()
    height = camera.getHeight()
    fov = camera.getFov()
    print(f"Camera enabled with resolution {width}x{height} and FOV {fov:.2f} radians.")


def control_robot(key, current_speed, steering_angle, devices, constants):
    if key == Keyboard.UP:
        current_speed = min(current_speed + constants["ACCELERATION"], constants["MAX_SPEED"])
    elif key == Keyboard.DOWN:
        current_speed = max(current_speed - constants["DECELERATION"], -constants["MAX_SPEED"])
    elif key == ord(' '):
        current_speed *= constants["BRAKE_INTENSITY"]

    if key == Keyboard.LEFT:
        steering_angle = max(steering_angle - 0.05, -constants["MAX_STEERING_ANGLE"])
    elif key == Keyboard.RIGHT:
        steering_angle = min(steering_angle + 0.05, constants["MAX_STEERING_ANGLE"])
    else:
        steering_angle *= 0.9

    devices["left_steer"].setPosition(steering_angle)
    devices["right_steer"].setPosition(steering_angle)
    devices["left_front_wheel"].setVelocity(current_speed)
    devices["right_front_wheel"].setVelocity(current_speed)

    return current_speed, steering_angle


def preprocess_image(camera):
    width = camera.getWidth()
    height = camera.getHeight()

    image = camera.getImage()
    image_array = np.frombuffer(image, dtype=np.uint8).reshape((height, width, 4))
    rgb_image = image_array[:, :, :3]

    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
    resized_image = cv2.resize(gray_image, (32, 14))
    flattened_image = resized_image.flatten()

    return flattened_image


def add_image_action_2_ds_optimized(camera, key_action, buffer):
    processed_image = preprocess_image(camera)

    action_mapping = {
        315: "F",
        314: "L",
        316: "R",
        32: "S"
    }
    action_label = action_mapping.get(key_action, "F")

    print(f"key_action: {key_action}, mapped_action: {action_label}")

    row = np.append(processed_image, action_label)
    buffer.append(row)

    return buffer


if __name__ == "__main__":
    robot, keyboard, timestep = initialize_robot()
    devices = get_devices(robot)

    configure_wheels(devices["left_front_wheel"], devices["right_front_wheel"])
    configure_camera(devices["camera"], timestep)

    constants = {
        "MAX_SPEED": 20.0,
        "MAX_STEERING_ANGLE": 0.5,
        "ACCELERATION": 1.0,
        "DECELERATION": 1.0,
        "BRAKE_INTENSITY": 0.8,
    }

    current_speed = 0.0
    steering_angle = 0.0
    buffer = []

    while robot.step(timestep) != -1:
        key = keyboard.getKey()

        buffer = add_image_action_2_ds_optimized(devices["camera"], key, buffer)

        current_speed, steering_angle = control_robot(
            key, current_speed, steering_angle, devices, constants
        )


    if buffer:
        try:
            file_exists = os.path.exists("custom_ds_of_webots_world.csv")
            with open("custom_ds_of_webots_world.csv", 'a') as f:
                pd.DataFrame(buffer).to_csv(f, header=not file_exists, index=False)

        except Exception as e:
            print(f"Error writing final data to file: {e}")
