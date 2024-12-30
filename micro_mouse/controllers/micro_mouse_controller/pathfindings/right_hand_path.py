def navigate_with_ir(ir_sensor_values, front_distance_threshold=10):
    """
    :param ir_sensor_values: E-puck's ir sensor values (a list with length of 8)
    :param front_distance_threshold: How much the robot can get close to the wall in front of it
    :return: 0 if it must go on straight, 1 if a turn to right is needed, 0 must turn to left
    """

    front_side = (ir_sensor_values[0] + ir_sensor_values[7]) / 2
    right_side = sum(ir_sensor_values[1: 3]) / 2
    left_side = sum(ir_sensor_values[5: 7]) / 2


    if right_side - left_side > 1: return 1
    elif right_side - left_side < 1: return 0
    elif front_side < front_distance_threshold: return -1


def navigate_with_custom_dist_sensor(dist_sensors, front_distance_threshold=0.1, turning_distance_threshold=0.6):
    front_side = dist_sensors[0]
    right_side = dist_sensors[1]
    rear_side = dist_sensors[2]
    left_side = dist_sensors[3]

    if ((front_side < 0.1 and right_side < 0.2) or
        (left_side > 0.2 and front_side > 0.25 and rear_side > 0.2)):
        return -1

    elif right_side < 0.2 and left_side < 0.2: return 0

    elif ((right_side > 0.7 or (right_side > 0.2 and left_side > 0.2) or
          (right_side > 0.2 and front_side > 0.25 and rear_side > 0.2)) or
          (front_side < 0.1 and right_side > 0.2)):
        return 1

    else: return 0
