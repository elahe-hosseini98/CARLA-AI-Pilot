"""obstacle_avoidance controller."""

from controller import Robot


def enable_sensors(robot: Robot, timestep: int):
    ps = []
    ps_names = ['ps' + str(i) for i in range(8)]

    for name in ps_names:
        sensor = robot.getDevice(name)
        sensor.enable(timestep)
        ps.append(sensor)

    return ps


def enable_camera(robot: Robot, timestep: int):
    camera = robot.getDevice('camera')
    camera.enable(timestep)

    return camera


def detect_obstacles_by_sensors(ps_list, max_speed: float, distance_threshold: float=90.0):
    ps_values = [sensor.getValue() for sensor in ps_list]
    
    print(ps_values) # these get higher as the robot gets closer to an obstacle

    right_obstacle = (ps_values[0] > distance_threshold
                      or ps_values[1] > distance_threshold
                      or ps_values[2] > distance_threshold)

    left_obstacle = (ps_values[5] > distance_threshold
                     or ps_values[6] > distance_threshold
                     or ps_values[7] > distance_threshold)

    if left_obstacle:
        return max_speed, -max_speed

    elif right_obstacle:
        return -max_speed, max_speed

    else:
        return max_speed, max_speed


def detect_obstacles_by_camera(camera_device, obstacle_threshold=80):
    image = camera_device.getImageArray()

    if image is None:
        return False

    height = camera_device.getHeight()
    width = camera_device.getWidth()

    grayscale = []
    for y in range(height):
        row = []
        for x in range(width):
            r = image[y][x][0]
            g = image[y][x][1]
            b = image[y][x][2]
            gray = (r + g + b) / 3
            row.append(gray)
        grayscale.append(row)

    grayscale = np.array(grayscale)

    central_region = grayscale[height // 3: 2 * height // 3, width // 3: 2 * width // 3]
    mean_intensity = np.mean(central_region)

    if mean_intensity < obstacle_threshold:
        return True
    else:
        return False


def start_engine(robot: Robot):
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')

    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

    return left_motor, right_motor


if __name__ == '__main__':
    epuck = Robot()

    timestep = int(epuck.getBasicTimeStep())

    max_speed = 6.28

    left_motor, right_motor = start_engine(epuck)

    ps_list = enable_sensors(epuck, timestep)
    camera = enable_camera(epuck, timestep)

    while epuck.step(timestep) != -1:

        left_speed, right_speed = detect_obstacles_by_sensors(ps_list, max_speed=max_speed)

        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)

