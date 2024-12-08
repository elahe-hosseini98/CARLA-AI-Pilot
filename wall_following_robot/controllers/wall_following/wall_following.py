"""wall_follower controller."""

from controller import Robot


def start_engine(robot: Robot, max_speed: float):
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')

    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    left_motor.setVelocity(max_speed)
    right_motor.setVelocity(max_speed)

    return left_motor, right_motor


def enable_sensors(robot: Robot):
    pass


def pid_controller():
    pass


def update_velocity():
    pass


def get_distance():
    pass


if __name__ == '__main__':
    epuck = Robot()

    MAX_SPEED = 6.28

    timestep = int(epuck.getBasicTimeStep())

    left_motor, right_motor = start_engine(robot=epuck, max_speed=MAX_SPEED)

    print(type(left_motor))

    while epuck.step(timestep) != -1:
        left_motor.setVelocity(MAX_SPEED)
        right_motor.setVelocity(MAX_SPEED)

