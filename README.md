# QuantTrade

QuantTrade is a comprehensive stock trading strategy project integrating multi-factor analysis, deep reinforcement learning, and GARCH models. This project covers data acquisition, data preprocessing, and model training modules to develop and optimize stock trading strategies.

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

The project was initially developed for competitions, aiming to build automated stock selection and trading strategies through the combination of multi-factor analysis, deep reinforcement learning, and financial time series models (like GARCH).

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
├── securities_list.py       # Script to generate stock list
├── securities_list.txt      # Stored stock list
├── securities_timing.py     # Experimental version of time series model
└── README.md                # Project description file
```

## Installation

Clone the repository to your local machine and install the necessary dependencies:

```sh
git clone https://github.com/QwenchC/QuantTrade.git
cd QuantTrade
pip install -r requirements.txt
```

## Usage

### 1. Data Acquisition

First, you need to acquire stock data from data sources such as JoinQuant or Tushare. Update your credentials in the respective scripts:

- Using JoinQuant data:

```sh
# Open data_acquisition-joinquant.py and update 'your_account' and 'your_password'
python data_acquisition-joinquant.py
```

- Using Tushare data:

```sh
# Open data_acquisition-tushare.py and update 'your_token'
python data_acquisition-tushare.py
```

Both scripts will save the raw data into the `data/` directory.

### 2. Data Preprocessing

Preprocess the raw data stored in the `data/` directory:

```sh
python data_preprocessing.py
```

Preprocessed data will be saved in the `preprocessing_data/` directory. This script performs the following tasks:
- Reads raw CSV data.
- Selects and renames columns (`trade_date` to `date`, and `vol` to `volume`).
- Converts date columns to datetime format.
- Saves the cleaned data back to CSV files in the `preprocessing_data/` directory.

### 3. Model Training

Depending on your hardware, you can choose to train the models using either CPU or GPU.

- Training models using CPU:

```sh
python cpu.py
```

- Training models using GPU:

```sh
python gpu.py
```

These scripts will:
- Load the preprocessed data from `preprocessing_data/`.
- Define and compile a LSTM (Long Short-Term Memory) model.
- Train the model using the preprocessed data.

Note: Ensure that the relevant GPU libraries are installed and configured if using the `gpu.py` script.

## Dependencies

The main Python libraries required for the QuantTrade project are listed below. Please refer to the `requirements.txt` file for a complete list of dependencies:

- `pandas`
- `numpy`
- `keras`
- `tushare`
- `jqdatasdk`

Install these dependencies using the following command:

```sh
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your modifications. For major changes, please open an issue first to discuss your plans.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
