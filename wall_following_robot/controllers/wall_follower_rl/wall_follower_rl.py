from controller import Robot
from Qlearning_agent import QLearningAgent
import numpy as np

class WallFollowerEnv:
    def __init__(self):
        self.robot = Robot()
        self.timestep = int(self.robot.getBasicTimeStep())
        self.max_speed = 6.28

        # Motors
        self.left_motor = self.robot.getDevice('left wheel motor')
        self.right_motor = self.robot.getDevice('right wheel motor')

        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))

        # Sensors
        self.ps = []
        ps_names = ['ps' + str(i) for i in range(8)]
        for name in ps_names:
            sensor = self.robot.getDevice(name)
            sensor.enable(self.timestep)
            self.ps.append(sensor)

        # RL-specific variables
        self.state_size = 6  # Reduced number of sensors used
        self.action_size = 3  # [Go straight, Turn left, Turn right]
        self.desired_distance = 10  # Ideal distance to maintain from the wall


    def reset(self):
        return self._get_state()


    def _get_state(self):
        ps_values = [self.ps[i].getValue() for i in [5, 6, 7, 0, 1, 2]]
        return np.array([1000 / ps_value for ps_value in ps_values])


    def step(self, action):
        reward = 0
        done = False

        if action == 0:
            self.left_motor.setVelocity(self.max_speed)
            self.right_motor.setVelocity(self.max_speed)
        elif action == 1:  # Turn left
            self.left_motor.setVelocity(0.5 * self.max_speed)
            self.right_motor.setVelocity(self.max_speed)
        elif action == 2:  # Turn right
            self.left_motor.setVelocity(self.max_speed)
            self.right_motor.setVelocity(0.5 * self.max_speed)

        if self.robot.step(self.timestep) == -1:
            done = True

        state = self._get_state()
        side_left = state[0]
        if side_left < self.desired_distance - 2:
            reward = -1  # Too close
        elif side_left > self.desired_distance + 2:
            reward = -1  # Too far
        else:
            reward = 1  # Desired distance maintained

        return state, reward, done


if __name__ == '__main__':
    env = WallFollowerEnv()
    agent = QLearningAgent(state_size=6, action_size=3)

    for episode in range(500):
        state = env.reset()
        state = tuple((state // 2).astype(int))
        total_reward = 0

        for step in range(1000):  # Max steps per episode
            action = agent.get_action(state)
            next_state, reward, done = env.step(action)
            next_state = tuple((next_state // 2).astype(int))
            agent.train(state, action, reward, next_state, done)

            state = next_state
            total_reward += reward
            if done:
                break

        print(f"Episode {episode + 1}, Total Reward: {total_reward}")

