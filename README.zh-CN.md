# QuantTrade

QuantTrade 是一个基于多因子分析、深度强化学习和GARCH模型的综合股票交易策略项目。它包括数据获取、数据预处理、模型训练等多个模块，旨在开发和优化股票交易策略。

## 目录

- [背景](#背景)
- [特性](#特性)
- [目录结构](#目录结构)
- [安装](#安装)
- [使用方法](#使用方法)
  - [1. 数据获取](#1-数据获取)
  - [2. 数据预处理](#2-数据预处理)
  - [3. 模型训练](#3-模型训练)
- [依赖](#依赖)
- [贡献](#贡献)
- [许可证](#许可证)

## 背景

项目曾用于某些竞赛，旨在结合多因子分析、深度强化学习和金融时间序列模型（如GARCH）构建自动化的股票选股和交易策略。

## 特性

- 多因子量化分析
- 深度强化学习模型
- GARCH模型
- 数据获取和预处理模块
- CPU和GPU模型训练支持

## 目录结构

```sh
QuantTrade/
├── data/                    # 原始数据存放目录
├── preprocessing_data/      # 预处理后数据存放目录
├── cpu.py                   # 使用CPU训练模型的脚本
├── data_acquisition-joinquant.py  # 用于从JoinQuant下载数据的脚本
├── data_acquisition-tushare.py    # 用于从Tushare下载数据的脚本
├── data_preprocessing.py    # 数据预处理脚本
├── gpu.py                   # 使用GPU训练模型的脚本
├── requirements.txt         # 依赖包列表
├── securities_list.py       # 生成股票列表的脚本
├── securities_list.txt      # 储存的股票列表
├── securities_timing.py     # 时序模型的实验版本
└── README.md                # 项目说明文件
```

## 安装

克隆仓库到本地并安装必要的依赖：

```sh
git clone https://github.com/QwenchC/QuantTrade.git
cd QuantTrade
pip install -r requirements.txt
```

## 使用方法

### 1. 数据获取

首先，你需要从数据源（如JoinQuant或Tushare）获取股票数据。

- 使用 JoinQuant 数据：

```sh
# 修改 data_acquisition-joinquant.py 中的账号信息
python data_acquisition-joinquant.py
```

- 使用 Tushare 数据：

```sh
# 修改 data_acquisition-tushare.py 中的 Token 信息
python data_acquisition-tushare.py
```


### 2. 数据预处理

获取到的原始数据存放在 `data/` 目录下，需要预处理：

```sh
python data_preprocessing.py
```

数据预处理后的结果会存储在 `preprocessing_data/` 目录下。

### 3. 模型训练

根据硬件情况选择使用CPU或GPU进行模型训练。

- 使用CPU训练模型：

```sh
python cpu.py
```

- 使用GPU训练模型：

```sh
python gpu.py
```

## 依赖

项目依赖的主要Python库如下，详细依赖请参考 `requirements.txt` 文件：

- `pandas`
- `numpy`
- `keras`
- `tushare`
- `jqdatasdk`

## 贡献

欢迎贡献！请 fork 本项目，并通过 pull request 提交修改。对于重大更改，请先提出 issue 以讨论您的计划。

## 许可证

本项目基于 MIT 许可证进行分发，详情请参阅 LICENSE 文件。
