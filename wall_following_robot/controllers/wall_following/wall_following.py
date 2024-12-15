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


def enable_sensors(robot: Robot, timestep: int):
    ps = []
    ps_names = ['ps' + str(i) for i in range(8)]

    for name in ps_names:
        sensor = robot.getDevice(name)
        sensor.enable(timestep)
        ps.append(sensor)

    return ps


def normalize_ps_values(ps_values):
    return [1000/ps_value for ps_value in ps_values]


def get_distance(ps_list):
    desired_ps_index = [5, 6, 7, 0, 1, 2]

    ps_values = [ps_list[i].getValue() for i in desired_ps_index]

    return normalize_ps_values(ps_values)


def update_velocity(ps_values, left_motor, right_motor, max_speed, found_wall, desired_distance=10):
    adjustment_speed = max_speed * 0.5

    def turn_right():
        left_motor.setVelocity(max_speed)
        right_motor.setVelocity(0)
        return True  # Wall found

    def turn_left():
        left_motor.setVelocity(0)
        right_motor.setVelocity(max_speed)

    def go_straight():
        left_motor.setVelocity(max_speed)
        right_motor.setVelocity(max_speed)

    def adjust_left():
        left_motor.setVelocity(adjustment_speed)
        right_motor.setVelocity(max_speed)

    def adjust_right():
        left_motor.setVelocity(max_speed)
        right_motor.setVelocity(adjustment_speed)

    front_left = ps_values[2]
    front_right = ps_values[3]
    side_left = ps_values[0]

    if front_left < desired_distance or front_right < desired_distance:
        print("big right")
        # Too close to the wall in front, turn right to avoid collision
        found_wall = turn_right()

    elif side_left > desired_distance and found_wall:
        print("small left")
        # Wall is too far on the left, move closer by turning left
        adjust_left()

    elif side_left < desired_distance:
        print("small right")
        # Wall is too close on the left, move away by turning right
        adjust_right()

    else:
        # Maintain the desired distance, move straight
        go_straight()

    return left_motor, right_motor, found_wall


if __name__ == '__main__':
    epuck = Robot()

    MAX_SPEED = 6.28

    timestep = int(epuck.getBasicTimeStep())

    left_motor, right_motor = start_engine(robot=epuck, max_speed=MAX_SPEED)

    enabled_ps = enable_sensors(robot=epuck, timestep=timestep)

    found_wall = False

    while epuck.step(timestep) != -1:
        ps_values = get_distance(enabled_ps)
        left_motor, right_motor, found_wall = update_velocity(ps_values, left_motor, right_motor, max_speed=MAX_SPEED, found_wall=found_wall)
        print(ps_values)
