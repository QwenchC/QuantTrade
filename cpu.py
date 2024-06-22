import os
import pandas as pd
import numpy as np
import gym
from gym import spaces
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random
from tqdm import tqdm  # 导入 tqdm 库

# 读取选出的股票
selected_stocks_path = 'data/selected.csv'
selected_stocks = pd.read_csv(selected_stocks_path)

# 获取股票代码列表
stock_codes = selected_stocks['stock_code'].tolist()

# 读取对应的股票历史数据
data_path = 'data/沪深A股'
stock_data = {}

for code in stock_codes:
    file_path = os.path.join(data_path, f'{code}_price_data.csv')
    stock_data[code] = pd.read_csv(file_path)

# 打印部分数据，确保正确读取
for code, data in stock_data.items():
    print(f'{code} data:')
    print(data.head())

class StockTradingEnv(gym.Env):
    def __init__(self, stock_data, initial_balance=1e7):
        super(StockTradingEnv, self).__init__()

        self.stock_data = stock_data
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.stock_codes = list(stock_data.keys())
        self.num_stocks = len(self.stock_codes)
        self.current_step = 0
        self.done = False
        self.held_stocks = {code: 0 for code in self.stock_codes}
        self.max_shares_per_stock = initial_balance * 0.3

        # 定义状态空间和动作空间
        self.action_space = spaces.MultiDiscrete([3] * self.num_stocks)
        self.observation_space = spaces.Box(low=0, high=1, shape=(self.num_stocks * 6 + 1,))

    def reset(self):
        self.current_balance = self.initial_balance
        self.current_step = 0
        self.done = False
        self.held_stocks = {code: 0 for code in self.stock_codes}
        return self._next_observation()

    def _next_observation(self):
        obs = []
        for code in self.stock_codes:
            data = self.stock_data[code].iloc[self.current_step]
            obs.extend([
                data['open'], data['close'], data['high'], data['low'], data['volume'], data['money']
            ])
        obs.append(self.current_balance)
        return np.array(obs) / np.array(obs).max()  # Normalize observation

    def step(self, actions):
        self._take_action(actions)
        self.current_step += 1

        if self.current_step >= len(self.stock_data[self.stock_codes[0]]) - 1:
            self.done = True

        reward = self._calculate_reward()
        obs = self._next_observation()

        return obs, reward, self.done, {}

    def _take_action(self, actions):
        for idx, action in enumerate(actions):
            code = self.stock_codes[idx]
            if action == 0:  # Hold
                continue
            elif action == 1:  # Buy
                shares_to_buy = self.max_shares_per_stock // self.stock_data[code].iloc[self.current_step]['close']
                cost = shares_to_buy * self.stock_data[code].iloc[self.current_step]['close']
                if self.current_balance >= cost:
                    self.current_balance -= cost
                    self.held_stocks[code] += shares_to_buy
            elif action == 2:  # Sell
                self.current_balance += self.held_stocks[code] * self.stock_data[code].iloc[self.current_step]['close']
                self.held_stocks[code] = 0

    def _calculate_reward(self):
        total_value = self.current_balance
        for code in self.stock_codes:
            total_value += self.held_stocks[code] * self.stock_data[code].iloc[self.current_step]['close']
        return total_value - self.initial_balance

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class Agent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.001
        self.model = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return [random.choice([0, 1, 2]) for _ in range(self.action_size // 3)]
        state = torch.FloatTensor(state).unsqueeze(0)
        act_values = self.model(state)
        return [torch.argmax(act_values[0][i:i+3]).item() for i in range(0, self.action_size, 3)]

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_state = torch.FloatTensor(next_state).unsqueeze(0)
                target = reward + self.gamma * torch.max(self.model(next_state)[0]).item()
            state = torch.FloatTensor(state).unsqueeze(0)
            target_f = self.model(state)
            for i, a in enumerate(action):
                target_f[0][i * 3 + a] = target
            self.optimizer.zero_grad()
            loss = nn.MSELoss()(self.model(state), target_f)
            loss.backward()
            self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# 定义并训练DQN
env = StockTradingEnv(stock_data)
agent = Agent(state_size=env.observation_space.shape[0], action_size=sum(env.action_space.nvec))

episodes = 1000
batch_size = 32

for e in tqdm(range(episodes), desc="Training Episodes"):  # 添加 tqdm 进度条
    state = env.reset()
    total_reward = 0
    for time in range(200):  # 假设一个月有200个交易时段
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        total_reward += reward
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        if done:
            print(f"Episode {e+1}/{episodes} - Total reward: {total_reward}")
            break
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
