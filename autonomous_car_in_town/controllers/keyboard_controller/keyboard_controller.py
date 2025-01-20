from controller import Robot, Keyboard

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
    }
    return devices


def configure_wheels(left_front_wheel, right_front_wheel):
    left_front_wheel.setPosition(float('inf'))
    right_front_wheel.setPosition(float('inf'))
    left_front_wheel.setVelocity(0)
    right_front_wheel.setVelocity(0)


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


if __name__ == "__main__":
    robot, keyboard, timestep = initialize_robot()
    devices = get_devices(robot)

    configure_wheels(devices["left_front_wheel"], devices["right_front_wheel"])

    constants = {
        "MAX_SPEED": 20.0,
        "MAX_STEERING_ANGLE": 0.5,
        "ACCELERATION": 1.0,
        "DECELERATION": 1.0,
        "BRAKE_INTENSITY": 0.8,
    }

    current_speed = 0.0
    steering_angle = 0.0

    while robot.step(timestep) != -1:
        key = keyboard.getKey()
        current_speed, steering_angle = control_robot(
            key, current_speed, steering_angle, devices, constants
        )
