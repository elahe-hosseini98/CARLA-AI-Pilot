from pathfindings.right_hand_path import navigate_with_custom_dist_sensor
from epuck_utils import read_robot_rotation


def keep_go_straight(robot, left_motor, right_motor, timestep, max_speed, turn_duration=0.4):
    start_time = robot.getTime()
    while robot.getTime() - start_time < turn_duration:
        left_motor.setVelocity(max_speed)
        right_motor.setVelocity(max_speed)
        robot.step(timestep)


def sharp_left_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration):
    print('Sharp turning to left')

    left_motor.setVelocity(-max_speed)
    right_motor.setVelocity(max_speed)

    start_time = robot.getTime()
    while robot.getTime() - start_time < turn_duration:
        robot.step(timestep)

    keep_go_straight(robot, left_motor, right_motor, timestep, max_speed)

    left_motor.setVelocity(max_speed)


def sharp_right_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration):
    print('Sharp turning to right')

    left_motor.setVelocity(max_speed)
    right_motor.setVelocity(-max_speed)

    start_time = robot.getTime()
    while robot.getTime() - start_time < turn_duration:
        robot.step(timestep)

    keep_go_straight(robot, left_motor, right_motor, timestep, max_speed)

    right_motor.setVelocity(max_speed)


def go_straight(robot, left_motor, right_motor, timestep, max_speed):
    print('go straight')
    left_motor.setVelocity(max_speed)
    right_motor.setVelocity(max_speed)

    keep_go_straight(robot, left_motor, right_motor, timestep, max_speed, turn_duration=0.2)


def turn_over(robot, left_motor, right_motor, timestep, max_speed, turn_duration):
    print('turn over')
    sharp_left_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration*2)
    keep_go_straight(robot, left_motor, right_motor, timestep, max_speed)


def update_velocity_based_on_path(robot, sensor_values, timestep, max_speed, prev_dir):
    turn_duration = 1.63

    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')

    direction = navigate_with_custom_dist_sensor(sensor_values, prev_dir=prev_dir) # 0: straight, 1: right, -1: left, 2: turn-over

    if direction == 0: # go straight
         go_straight(robot, left_motor, right_motor, timestep, max_speed)

    elif direction == 1: # turn right
         sharp_right_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration)

    elif direction == -1: # turn left
         sharp_left_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration)

    else: # turn over
        turn_over(robot, left_motor, right_motor, timestep, max_speed, turn_duration)

    prev_dir = direction

    return direction, prev_dir