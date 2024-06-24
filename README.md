# QuantTrade

QuantTrade is a comprehensive stock trading strategy project based on multi-factor analysis, deep reinforcement learning, and GARCH models. It includes modules for data acquisition, data preprocessing, and model training, aiming to develop and optimize stock trading strategies.

## Table of Contents

- [Background](#background)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [1. Data Acquisition](#1-data-acquisition)
  - [2. Data Preprocessing](#2-data-preprocessing)
  - [3. Model Training](#3-model-training)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Background

The project was originally used in competitions and aims to build automated stock selection and trading strategies by combining multi-factor analysis, deep reinforcement learning, and financial time series models such as GARCH.

## Features

- Multi-factor quantitative analysis
- Deep reinforcement learning models
- GARCH model
- Data acquisition and preprocessing modules
- Support for CPU and GPU model training

## Directory Structure

```sh
QuantTrade/
├── data/                    # Raw data directory
├── preprocessing_data/      # Preprocessed data directory
├── cpu.py                   # Script for training models using CPU
├── data_acquisition-joinquant.py  # Script for downloading data from JoinQuant
├── data_acquisition-tushare.py    # Script for downloading data from Tushare
├── data_preprocessing.py    # Data preprocessing script
├── gpu.py                   # Script for training models using GPU
├── requirements.txt         # List of dependencies
├── securities_list.py       # Script
