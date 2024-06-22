import os
import pandas as pd
import numpy as np
import gym
from gym import spaces
from stable_baselines3 import DQN


class StockTradingEnv(gym.Env):
    def __init__(self, stock_data, initial_balance=1_000_000, max_stock_percent=0.3):
        super(StockTradingEnv, self).__init__()

        self.stock_data = stock_data
        self.initial_balance = initial_balance
        self.max_stock_percent = max_stock_percent
        self.current_step = 0
        self.n_steps = len(stock_data)

        self.action_space = spaces.Discrete(3)  # 0: hold, 1: buy, 2: sell
        self.observation_space = spaces.Box(low=0, high=1, shape=(6,), dtype=np.float32)

        self.reset()

    def reset(self):
        self.balance = self.initial_balance
        self.stock_held = 0
        self.stock_price = self.stock_data['close'].values[self.current_step]
        self.total_asset = self.balance
        self.current_step = 0

        return self._get_observation()

    def _get_observation(self):
        obs = [
            self.balance / self.initial_balance,
            self.stock_held / (self.initial_balance / self.stock_price),
            self.stock_price / self.stock_data['close'].max(),
            self.stock_data['open'].values[self.current_step] / self.stock_data['close'].max(),
            self.stock_data['high'].values[self.current_step] / self.stock_data['close'].max(),
            self.stock_data['low'].values[self.current_step] / self.stock_data['close'].max()
        ]
        return np.array(obs)

    def step(self, action):
        self.stock_price = self.stock_data['close'].values[self.current_step]
        prev_total_asset = self.total_asset

        if action == 1:  # Buy
            max_buy = self.balance // self.stock_price
            buy_amount = min(max_buy, (self.initial_balance * self.max_stock_percent) // self.stock_price)
            self.balance -= buy_amount * self.stock_price
            self.stock_held += buy_amount
        elif action == 2:  # Sell
            self.balance += self.stock_held * self.stock_price
            self.stock_held = 0

        self.total_asset = self.balance + self.stock_held * self.stock_price
        self.current_step += 1
        done = self.current_step >= self.n_steps - 1
        reward = self.total_asset - prev_total_asset
        obs = self._get_observation()

        return obs, reward, done, {}

    def render(self, mode='human', close=False):
        print(f'Step: {self.current_step}')
        print(f'Balance: {self.balance}')
        print(f'Stock Held: {self.stock_held}')
        print(f'Total Asset: {self.total_asset}')

# Load selected stocks data
selected_stocks = pd.read_csv('data/selected.csv')
selected_stock_codes = selected_stocks['stock_code'].values

# Prepare stock data for the environment
data_path = 'data/沪深A股'
stock_data_list = []
for code in selected_stock_codes:
    file_path = os.path.join(data_path, f"{code}_price_data.csv")
    stock_data = pd.read_csv(file_path)
    stock_data_list.append(stock_data)

# Here, assuming we use the first stock for simplicity
stock_data = stock_data_list[0]

# Initialize the environment
env = StockTradingEnv(stock_data)

# Initialize DQN agent
model = DQN('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=10_000)

# Save the model
model.save('dqn_stock_trading')

# Load the trained model
model = DQN.load('dqn_stock_trading')

# Test the trained model
obs = env.reset()
for _ in range(len(stock_data) - 1):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
    if done:
        break

obs = env.reset()
for _ in range(len(stock_data) - 1):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
    if done:
        break
