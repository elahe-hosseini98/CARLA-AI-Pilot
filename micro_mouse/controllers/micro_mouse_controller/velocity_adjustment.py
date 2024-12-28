from pathfindings.right_hand_path import navigate_with_ir, navigate_with_custom_dist_sensor


def sharp_left_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration):
    print('turn left')
    left_motor.setVelocity(-max_speed)
    right_motor.setVelocity(max_speed)

    start_time = robot.getTime()
    while robot.getTime() - start_time < turn_duration:
        robot.step(timestep)

    left_motor.setVelocity(max_speed)
    right_motor.setVelocity(max_speed)


def sharp_right_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration):
    print('turn right')
    left_motor.setVelocity(max_speed)
    right_motor.setVelocity(-max_speed)

    start_time = robot.getTime()
    while robot.getTime() - start_time < turn_duration:
        robot.step(timestep)

    left_motor.setVelocity(max_speed)
    right_motor.setVelocity(max_speed)


def go_straight(left_motor, right_motor, max_speed):
    print('go straight')
    left_motor.setVelocity(max_speed)
    right_motor.setVelocity(max_speed)


def update_velocity_based_on_path(robot, ir_sensor_values, timestep, max_speed):
    turn_duration = 1.632

    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')

    direction = navigate_with_custom_dist_sensor(ir_sensor_values) # 0: straight, 1: right, -1: left

    if direction == 0: # go straight
        return go_straight(left_motor, right_motor, max_speed)

    elif direction == 1: # turn right
        return sharp_right_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration)

    else: # turn left
        return sharp_left_turn(robot, left_motor, right_motor, timestep, max_speed, turn_duration)