from autonomous_arena.pretraned_model_loader import load_pretrained_model, predict_new_action
from autonomous_arena.fine_tuning_on_costum_ds import fine_tuning
from controller import Robot, Keyboard
import numpy as np


def initialize_robot():
    robot = Robot()
    keyboard = Keyboard()
    timestep = int(robot.getBasicTimeStep())
    keyboard.enable(timestep)
    return robot, keyboard, timestep


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


def make_decision_based_on_camera(model, camera):
    width = camera.getWidth()
    height = camera.getHeight()

    image = camera.getImage()
    image_array = np.frombuffer(image, dtype=np.uint8).reshape((height, width, 4))
    rgb_image = image_array[:, :, :3]

    prediction = predict_new_action(model, rgb_image)

    return prediction


def control_robot(new_action, current_speed, steering_angle, devices, constants):
    print("new action: ", new_action)
    if new_action == 1: # must be 0
        current_speed = min(current_speed + constants["ACCELERATION"], constants["MAX_SPEED"])

    elif new_action == Keyboard.DOWN:
        current_speed = max(current_speed - constants["DECELERATION"], -constants["MAX_SPEED"])

    elif new_action == 2:
        current_speed *= constants["BRAKE_INTENSITY"]

    elif new_action == 3:
        steering_angle = max(steering_angle - 0.05, -constants["MAX_STEERING_ANGLE"])

    elif new_action == 0:
        steering_angle = min(steering_angle + 0.05, constants["MAX_STEERING_ANGLE"])

    else:
        steering_angle *= 0.9

    devices["left_steer"].setPosition(steering_angle)
    devices["right_steer"].setPosition(steering_angle)
    devices["left_front_wheel"].setVelocity(current_speed)
    devices["right_front_wheel"].setVelocity(current_speed)

    return current_speed, steering_angle


if __name__ == '__main__':
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

    path_2_pretrained_model = "autonomous_arena/autonomous_arena_pretrained_model.pth"
    pretrained_model = load_pretrained_model(path_2_pretrained_model)

    path_2_custom_ds = "../keyboard_controller/custom_ds_of_webots_world.csv"
    fine_tuned_model = fine_tuning(pretrained_model, path_2_custom_ds)

    while robot.step(timestep) != -1:
        new_action = make_decision_based_on_camera(fine_tuned_model, devices["camera"])

        current_speed, steering_angle = control_robot(
            new_action, current_speed, steering_angle, devices, constants
        )