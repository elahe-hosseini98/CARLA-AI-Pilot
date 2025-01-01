from controller import Robot
from pathlib import Path
import pandas as pd


def read_robot_rotation(robot: Robot):
    inertial_unit = robot.getDevice("inertial unit")
    inertial_unit.enable(int(robot.getBasicTimeStep()))

    rotation = inertial_unit.getRollPitchYaw()

    _, _, yaw = rotation
    return yaw


def add_timestep_details_2_excel(robot: Robot, dist_sensors):
    front_side = round(dist_sensors[0], 2)
    right_side = round(dist_sensors[1], 2)
    rear_side = round(dist_sensors[2], 2)
    left_side = round(dist_sensors[3], 2)
    yaw = round(read_robot_rotation(robot), 2)

    file_path = Path("data_pipeline/data/robot_navigation_data.xlsx")

    if file_path.exists():
        data = pd.read_excel(file_path)
    else:
        data = pd.DataFrame(columns=["front-dist", "right-dist", "rear-dist", "left-dist", "yaw"])

    new_row = {
        "front-dist": front_side,
        "right-dist": right_side,
        "rear-dist": rear_side,
        "left-dist": left_side,
        "yaw": yaw,
        "direction": 0
    }

    data = data.append(new_row, ignore_index=True)
    data.to_excel(file_path, index=False)

    print(f"yaw={yaw:.2f}, dist_sensors={dist_sensors}")






