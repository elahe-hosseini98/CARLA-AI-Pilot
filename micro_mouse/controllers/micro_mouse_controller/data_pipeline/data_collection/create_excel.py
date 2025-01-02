from sklearn.utils import resample
from controller import Robot
from pathlib import Path
import pandas as pd
import os


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


def create_balanced_excel(input_path):
    df = pd.read_excel(input_path)

    class_counts = df['direction'].value_counts()
    target_samples_per_class = class_counts.max()

    def upsample_class(df, target_class, target_count):
        class_data = df[df['direction'] == target_class]
        if len(class_data) < target_count:
            upsampled_data = resample(
                class_data,
                replace=True,
                n_samples=target_count,
                random_state=42
            )
        else:
            upsampled_data = class_data
        return upsampled_data

    balanced_data = pd.concat(
        [upsample_class(df, direction, target_samples_per_class) for direction in class_counts.index],
        ignore_index=True
    )

    balanced_data = balanced_data.sample(frac=1, random_state=42).reset_index(drop=True)

    output_path = os.path.splitext(input_path)[0] + "_balanced.xlsx"
    balanced_data.to_excel(output_path, index=False)

    print(f"Balanced excel file created successfully at {output_path}!")


def downsample_data(file_path, output_file_name="downsampled_robot_navigation_data.xlsx"):
    data = pd.read_excel(file_path)

    direction_zero_data = data[data['direction'] == 0]

    unique_yaws = direction_zero_data['yaw'].unique()

    samples_per_yaw = 50 // len(unique_yaws)

    downsampled_data = pd.DataFrame()
    for yaw in unique_yaws:
        yaw_data = direction_zero_data[direction_zero_data['yaw'] == yaw]
        downsampled_data = pd.concat(
            [downsampled_data, yaw_data.sample(n=min(samples_per_yaw, len(yaw_data)), random_state=42)])

    remaining_data = data[data['direction'] != 0]
    final_data = pd.concat([remaining_data, downsampled_data]).reset_index(drop=True)

    output_file_path = os.path.join(os.path.dirname(file_path), output_file_name)
    final_data.to_excel(output_file_path, index=False)

    print("Down-sampled excel file created successfully")


if __name__ == "__main__":
    original_rexcel_path = "../data/robot_navigation_data.xlsx"

    create_balanced_excel(original_rexcel_path)
    downsample_data(original_rexcel_path)






