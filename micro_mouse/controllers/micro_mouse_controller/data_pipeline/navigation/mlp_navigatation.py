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
    right_motor.setVelocity(-max_speed)


def go_straight(robot, left_motor, right_motor, timestep, max_speed):
    #print('go straight')
    left_motor.setVelocity(max_speed)
    right_motor.setVelocity(max_speed)

    keep_go_straight(robot, left_motor, right_motor, timestep, max_speed, turn_duration=0.2)


def mlp_navigate(robot, timestep, max_speed, new_direction, prev_yaw):
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')

    if new_direction == 0:
        go_straight(robot, left_motor, right_motor, timestep, max_speed)
        new_yaw =  prev_yaw

    elif new_direction == 1:
        sharp_right_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration=1.63)
        new_yaw = prev_yaw - 1.57

    else:
        sharp_left_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration=1.63)
        new_yaw = prev_yaw + 1.57

    return new_yaw
