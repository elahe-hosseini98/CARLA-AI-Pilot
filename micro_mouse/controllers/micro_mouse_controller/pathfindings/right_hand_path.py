def navigate_with_custom_dist_sensor(dist_sensors, prev_dir):
    front_side = dist_sensors[0]
    right_side = dist_sensors[1]
    rear_side = dist_sensors[2]
    left_side = dist_sensors[3]


    if prev_dir == 1:
        return 0

    if right_side < 0.1 and left_side < 0.1 and front_side > 0.07:
        return 0

    if right_side < 0.1 and left_side < 0.1 and front_side < 0.07:
        return 2

    if right_side < 0.15 and front_side < 0.1:
        return -1

    if right_side > 0.5:
        return 1

    if 0.15 < right_side and front_side < 0.1:
        return 1

    if 0.24 < right_side < 0.3:
        return 1

    return 0



