import gym
from gym import spaces
import numpy as np
import pandas as pd
from stable_baselines3 import PPO

class StockTradingEnv(gym.Env):
    def __init__(self, df):
        super(StockTradingEnv, self).__init__()

        self.df = df
        self.action_space = spaces.Discrete(3)  # 0: hold, 1: buy, 2: sell
        self.observation_space = spaces.Box(low=0, high=1, shape=(6,), dtype=np.float32)

        self.current_step = 0
        self.stock_owned = 0
        self.cash_in_hand = 10000

    def reset(self):
        self.current_step = 0
        self.stock_owned = 0
        self.cash_in_hand = 10000
        return self._next_observation()

    def _next_observation(self):
        frame = np.array([
            self.df.loc[self.current_step, 'open'],
            self.df.loc[self.current_step, 'high'],
            self.df.loc[self.current_step, 'low'],
            self.df.loc[self.current_step, 'close'],
            self.df.loc[self.current_step, 'volume'],
            self.cash_in_hand
        ])
        return frame

    def step(self, action):
        self.current_step += 1

        if action == 1:  # buy
            self.stock_owned += 1
            self.cash_in_hand -= self.df.loc[self.current_step, 'close']
        elif action == 2:  # sell
            self.stock_owned -= 1
            self.cash_in_hand += self.df.loc[self.current_step, 'close']

        reward = self.stock_owned * self.df.loc[self.current_step, 'close'] + self.cash_in_hand
        done = self.current_step == len(self.df) - 1
        obs = self._next_observation()

        return obs, reward, done, {}

    def render(self, mode='human'):
        pass

# Load data
df = pd.read_csv('path_to_your_csv_file.csv')

# Initialize environment
env = StockTradingEnv(df)

# Initialize and train the model
model = PPO('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=20000)

# Evaluate the model
obs = env.reset()
for _ in range(len(df)):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    if done:
        break
