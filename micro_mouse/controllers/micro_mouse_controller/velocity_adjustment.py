from pathfindings.right_hand_path import navigate_with_ir, navigate_with_custom_dist_sensor


def keep_go_straight(robot, left_motor, right_motor, timestep, max_speed, turn_duration=0.4):
    start_time = robot.getTime()
    while robot.getTime() - start_time < turn_duration:
        left_motor.setVelocity(max_speed)
        right_motor.setVelocity(max_speed)
        robot.step(timestep)


def sharp_left_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration):
    #print('Sharp turning to left')

    left_motor.setVelocity(-max_speed)
    right_motor.setVelocity(max_speed)

    start_time = robot.getTime()
    while robot.getTime() - start_time < turn_duration:
        robot.step(timestep)

    keep_go_straight(robot, left_motor, right_motor, timestep, max_speed)

    left_motor.setVelocity(max_speed)


def sharp_right_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration):
    #print('Sharp turning to right')

    left_motor.setVelocity(max_speed)
    right_motor.setVelocity(-max_speed)

    start_time = robot.getTime()
    while robot.getTime() - start_time < turn_duration:
        robot.step(timestep)

    keep_go_straight(robot, left_motor, right_motor, timestep, max_speed)

    right_motor.setVelocity(max_speed)


def smooth_left_turn(left_motor, right_motor, max_speed):
    print('Smooth turning to left')

    left_motor.setVelocity(-max_speed)
    right_motor.setVelocity(max_speed)


def smooth_right_turn(left_motor, right_motor, max_speed):
    print('Smooth turning to right')

    left_motor.setVelocity(max_speed)
    right_motor.setVelocity(-max_speed)


def go_straight(robot, left_motor, right_motor, timestep, max_speed):
    #print('go straight')
    left_motor.setVelocity(max_speed)
    right_motor.setVelocity(max_speed)

    keep_go_straight(robot, left_motor, right_motor, timestep, max_speed, turn_duration=0.2)


def update_velocity_based_on_path(robot, sensor_values, timestep, max_speed):
    turn_duration = 1.63

    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')

    direction = navigate_with_custom_dist_sensor(sensor_values) # 0: straight, 1: right, -1: left

    if direction == 0: # go straight
         go_straight(robot, left_motor, right_motor, timestep, max_speed)

    elif direction == 1: # turn right
         sharp_right_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration)

    else: # turn left
         sharp_left_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration)

    return direction
