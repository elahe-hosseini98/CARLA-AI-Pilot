from controller import Robot
import numpy as np
import cv2


def initialize_robot():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())
    return robot, timestep


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


def display_camera(camera):
    width = camera.getWidth()
    height = camera.getHeight()

    while True:
        image = camera.getImage()

        if image:
            image_array = np.frombuffer(image, dtype=np.uint8).reshape((height, width, 4))
            rgb_image = image_array[:, :, :3]
            cv2.imshow("Camera View", rgb_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    robot, timestep = initialize_robot()
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

    while robot.step(timestep) != -1:
        display_camera(devices["camera"])