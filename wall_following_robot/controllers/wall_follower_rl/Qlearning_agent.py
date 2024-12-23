import numpy as np

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.99, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.q_table = np.zeros((state_size ** 3, action_size))  # Simplify by discretizing states

    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.action_size)  # Explore
        return np.argmax(self.q_table[tuple(state)])  # Exploit

    def train(self, state, action, reward, next_state, done):
        old_value = self.q_table[tuple(state)][action]
        next_max = np.max(self.q_table[tuple(next_state)])
        new_value = old_value + self.learning_rate * (reward + self.discount_factor * next_max * (1 - done) - old_value)
        self.q_table[tuple(state)][action] = new_value

        if done and self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay