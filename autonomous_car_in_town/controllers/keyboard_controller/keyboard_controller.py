from controller import Robot, Keyboard

# Initialize robot and keyboard
robot = Robot()
keyboard = Keyboard()

# Time step for the simulation
timestep = int(robot.getBasicTimeStep())
keyboard.enable(timestep)

# Get device handles
left_steer = robot.getDevice("left_steer")
right_steer = robot.getDevice("right_steer")
engine_speaker = robot.getDevice("engine_speaker")

# Wheel motors for driving
left_front_wheel = robot.getDevice("left_front_wheel")
right_front_wheel = robot.getDevice("right_front_wheel")

# Brakes
left_front_brake = robot.getDevice("left_front_brake")
right_front_brake = robot.getDevice("right_front_brake")

# Set initial configurations
left_front_wheel.setPosition(float('inf'))  # Infinite position for continuous rotation
right_front_wheel.setPosition(float('inf'))
left_front_wheel.setVelocity(0)  # Initial velocity
right_front_wheel.setVelocity(0)

# Parameters
MAX_SPEED = 20.0  # Max wheel velocity in m/s
MAX_STEERING_ANGLE = 0.5  # Max steering angle in radians
ACCELERATION = 1.0  # Speed increment per timestep
DECELERATION = 1.0  # Speed decrement per timestep
BRAKE_INTENSITY = 0.8  # Brake intensity factor

# Control variables
current_speed = 0.0
steering_angle = 0.0

# Main control loop
while robot.step(timestep) != -1:
    key = keyboard.getKey()

    print(key)

    # Handle speed controls
    if key == Keyboard.UP:
        current_speed = min(current_speed + ACCELERATION, MAX_SPEED)
    elif key == Keyboard.DOWN:
        current_speed = max(current_speed - DECELERATION, -MAX_SPEED)
    elif key == ord(' '):  # Spacebar for braking
        current_speed *= BRAKE_INTENSITY

    # Handle steering controls
    if key == Keyboard.LEFT:
        steering_angle = max(steering_angle - 0.05, -MAX_STEERING_ANGLE)
    elif key == Keyboard.RIGHT:
        steering_angle = min(steering_angle + 0.05, MAX_STEERING_ANGLE)
    else:
        # Gradual reset of steering angle when no key is pressed
        steering_angle *= 0.9

    # Apply controls to devices
    left_steer.setPosition(steering_angle)  # Set steering angle for left wheel
    right_steer.setPosition(steering_angle)  # Set steering angle for right wheel
    left_front_wheel.setVelocity(current_speed)  # Set velocity for left front wheel
    right_front_wheel.setVelocity(current_speed)  # Set velocity for right front wheel
