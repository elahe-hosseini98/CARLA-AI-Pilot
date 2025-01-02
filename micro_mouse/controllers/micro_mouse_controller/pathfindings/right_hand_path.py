def navigate_with_custom_dist_sensor(dist_sensors):
    front_side = dist_sensors[0]
    right_side = dist_sensors[1]
    rear_side = dist_sensors[2]
    left_side = dist_sensors[3]

    if ((front_side < 0.1 and right_side < 0.2) or
        (left_side > 0.2 and front_side > 0.25 and rear_side > 0.2)):
        return -1

    elif right_side < 0.2 and left_side < 0.2: return 0

    elif ((right_side > 0.7 or (right_side > 0.2 and left_side > 0.2) or
          (right_side > 0.25 and front_side > 0.25 and rear_side > 0.2)) or
          (front_side < 0.1 and right_side > 0.2)):
        return 1

    else: return 0
