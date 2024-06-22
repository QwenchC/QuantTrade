import os
from jqdatasdk import auth, get_all_securities, get_price, get_fundamentals, query, valuation, balance, income, indicator
from tqdm import tqdm

# 登录聚宽
auth('your_username', 'your_password')

# 创建 data 文件夹和子文件夹，如果不存在的话
folders = ['data', 'data/沪深A股', 'data/场内基金', 'data/股指期货']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# 获取沪深A股基本信息
stocks = get_all_securities(types=['stock'])
stocks_filtered = stocks[(stocks['end_date'] > '2024-01-01') & (~stocks['display_name'].str.contains('ST'))]
stocks_filtered = stocks_filtered.head(100)

# 获取场内基金基本信息
funds = get_all_securities(types=['etf'])
funds_filtered = funds.head(100)

# 获取股指期货基本信息
futures = get_all_securities(types=['futures'])
futures_filtered = futures.head(100)

# 定义下载历史行情数据的时间范围
start_date = '2020-01-01'
end_date = '2024-01-01'

# 下载沪深A股数据
with tqdm(total=len(stocks_filtered), desc="Downloading stock data", unit="stock") as pbar:
    for stock_code in stocks_filtered.index:
        try:
            price_data = get_price(stock_code, start_date=start_date, end_date=end_date, frequency='daily')
            price_data.to_csv(f'data/沪深A股/{stock_code}_price_data.csv', index=True)
        except Exception as e:
            print(f"{stock_code} 数据下载失败: {e}")
        finally:
            pbar.update(1)

# 下载场内基金数据
with tqdm(total=len(funds_filtered), desc="Downloading fund data", unit="fund") as pbar:
    for fund_code in funds_filtered.index:
        try:
            price_data = get_price(fund_code, start_date=start_date, end_date=end_date, frequency='daily')
            price_data.to_csv(f'data/场内基金/{fund_code}_price_data.csv', index=True)
        except Exception as e:
            print(f"{fund_code} 数据下载失败: {e}")
        finally:
            pbar.update(1)

# 下载股指期货数据
with tqdm(total=len(futures_filtered), desc="Downloading futures data", unit="future") as pbar:
    for future_code in futures_filtered.index:
        try:
            price_data = get_price(future_code, start_date=start_date, end_date=end_date, frequency='daily')
            price_data.to_csv(f'data/股指期货/{future_code}_price_data.csv', index=True)
        except Exception as e:
            print(f"{future_code} 数据下载失败: {e}")
        finally:
            pbar.update(1)

print("所有股票、场内基金和股指期货历史行情数据保存成功")