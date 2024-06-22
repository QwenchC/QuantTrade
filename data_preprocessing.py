import os
import pandas as pd

## 数据获取
# 定义数据路径
data_path = 'data/沪深A股'

# 获取所有CSV文件
files = [f for f in os.listdir(data_path) if f.endswith('_price_data.csv')]

# 打印所有文件名，确保文件被正确读取
print("Files found in directory:")
print(files)

# 创建一个空的列表来存储所有数据
all_data_list = []

# 遍历文件并读取数据
for file in files:
    file_path = os.path.join(data_path, file)
    print(f"Reading file: {file_path}")  # 打印当前读取的文件路径
    stock_data = pd.read_csv(file_path)
    stock_data['stock_code'] = file.split('_')[0]  # 从文件名中提取股票代码
    print(stock_data.head())  # 打印读取的部分内容
    all_data_list.append(stock_data)

# 使用 pd.concat() 将所有数据拼接起来
all_data = pd.concat(all_data_list, ignore_index=True)

# 打印拼接后的数据
print(all_data.head())
print(all_data['stock_code'].unique())  # 打印所有唯一的股票代码

## 特征工程
# 基本面因子
# 加载基本面数据
fundamentals_path = 'data/沪深A股/fundamentals.csv'
fundamentals = pd.read_csv(fundamentals_path)

# 打印基本面数据的列名，确保包含 'code' 列
print("Fundamentals columns:")
print(fundamentals.columns)

# 将 'fundamentals' 中的 'code' 列重命名为 'stock_code'
fundamentals.rename(columns={'code': 'stock_code'}, inplace=True)

# 合并基本面数据
all_data = all_data.merge(fundamentals, on='stock_code', how='left')

# 技术面因子
# 计算移动平均线
all_data['ma_5'] = all_data.groupby('stock_code')['close'].transform(lambda x: x.rolling(window=5).mean())
all_data['ma_20'] = all_data.groupby('stock_code')['close'].transform(lambda x: x.rolling(window=20).mean())

# 计算相对强弱指数（RSI）
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

all_data['rsi_14'] = all_data.groupby('stock_code')['close'].transform(lambda x: calculate_rsi(x))

# 计算动量
all_data['momentum'] = all_data.groupby('stock_code')['close'].transform(lambda x: x - x.shift(10))

# 情绪因子
# 计算换手率
all_data['turnover_rate'] = all_data['volume'] / all_data['volume'].rolling(window=20).mean()

## 数据清洗与处理
# 删除含有缺失值的行
all_data.dropna(inplace=True)

# 保存处理后的数据
output_path = 'preprocessing_data'
os.makedirs(output_path, exist_ok=True)
all_data.to_csv(os.path.join(output_path, 'processed_data.csv'), index=False)
