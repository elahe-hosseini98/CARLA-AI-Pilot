from controller import Robot


def start_engine(robot: Robot, max_speed: float):
    left_motor = robot.getDevice("motor.left")
    right_motor = robot.getDevice("motor.right")

    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    left_motor.setVelocity(max_speed)
    right_motor.setVelocity(max_speed)

    return left_motor, right_motor


def active_distance_sensors(robot: Robot, timestep):
    distance_sensors = []

    sensor_names = ['prox.horizontal.' + str(i) for i in range(5)]

    for name in sensor_names:
        sensor = robot.getDevice(name)
        sensor.enable(timestep)
        distance_sensors.append(sensor)

    return distance_sensors


def active_ground_sensors(robot: Robot, timestep):
    ground_sensors = []

    sensor_names = ['prox.ground.' + str(i) for i in range(2)]

    for name in sensor_names:
        sensor = robot.getDevice(name)
        sensor.enable(timestep)
        ground_sensors.append(sensor)

    return ground_sensors


def normalize_ps_values(ps_values):
    return [1000/ps_value for ps_value in ps_values]


def get_distance_sensors_values(distance_sensors):
    distance_values = [distance_sensor.getValue() for distance_sensor in distance_sensors]
    return normalize_ps_values(distance_values)


def get_ground_sensors_values(ground_sensors):
    ground_distance_values = [ground_sensor.getValue() for ground_sensor in ground_sensors]
    return normalize_ps_values(ground_distance_values)


def update_velocity(robot: Robot, max_speed: float):
    ...


if __name__ == '__main__':
    robot = Robot()

    timeStep = int(robot.getBasicTimeStep())

    max_speed = 6

    start_engine(robot, max_speed)
    active_distance_sensors(robot, timeStep)
    active_ground_sensors(robot, timeStep)

    activated_distance_sensors = active_distance_sensors(robot, timeStep)
    activated_ground_sensors = active_ground_sensors(robot, timeStep)

    while robot.step(timeStep) != -1:
        distance_values = get_distance_sensors_values(activated_distance_sensors)
        ground_distance_values = get_ground_sensors_values(activated_ground_sensors)

        print(ground_distance_values)




