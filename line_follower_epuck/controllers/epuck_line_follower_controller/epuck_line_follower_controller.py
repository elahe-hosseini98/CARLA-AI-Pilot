from controller import Robot

def run_robot(robot):
    time_step = int(robot.getBasicTimeStep())
    max_speed = 6.28

    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

    left_light_sensor = robot.getDevice('ir0')
    right_light_sensor = robot.getDevice('ir1')
    left_light_sensor.enable(time_step)
    right_light_sensor.enable(time_step)

    while robot.step(time_step) != -1:
        left_value = left_light_sensor.getValue()
        right_value = right_light_sensor.getValue()

        print(f"Left Sensor: {left_value}, Right Sensor: {right_value}")

        # Determine threshold based on sensor readings
        threshold = (left_value + right_value) / 2

        # Implement line-following logic
        if left_value < threshold and right_value >= threshold:
            # Turn left
            left_speed = max_speed * 0.5
            right_speed = max_speed
        elif right_value < threshold and left_value >= threshold:
            # Turn right
            left_speed = max_speed
            right_speed = max_speed * 0.5
        else:
            # Move forward
            left_speed = max_speed
            right_speed = max_speed

        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)

if __name__ == '__main__':
    epuck = Robot()
    run_robot(epuck)
