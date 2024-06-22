import tushare as ts
import os

# 设置你的 Tushare API Token
ts.set_token('your api key')
pro = ts.pro_api()

# 创建 data 文件夹，如果不存在的话
if not os.path.exists('data'):
    os.makedirs('data')

try:
    # 获取沪深A股基本信息（不包含退市整理板块和ST板块）
    stock_basic = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market,list_date')
    stock_basic = stock_basic[~stock_basic['name'].str.contains('ST')]  # 过滤掉ST股票
    stock_basic.to_csv('data/stock_basic.csv', index=False)
    print("沪深A股基本信息获取并保存成功")
except Exception as e:
    print(f"获取沪深A股基本信息时发生错误: {e}")

try:
    # 获取科创板股票基本信息
    sci_tech_board = pro.stock_basic(exchange='', list_status='L', market='科创板', fields='ts_code,symbol,name,area,industry,market,list_date')
    sci_tech_board = sci_tech_board[~sci_tech_board['name'].str.contains('ST')]  # 过滤掉ST股票
    sci_tech_board.to_csv('data/sci_tech_board.csv', index=False)
    print("科创板股票基本信息获取并保存成功")
except Exception as e:
    print(f"获取科创板股票基本信息时发生错误: {e}")

try:
    # 获取场内基金基本信息
    fund_basic = pro.fund_basic(market='E')
    fund_basic.to_csv('data/fund_basic.csv', index=False)
    print("场内基金基本信息获取并保存成功")
except Exception as e:
    print(f"获取场内基金基本信息时发生错误: {e}")

try:
    # 获取股指期货基本信息
    fut_basic = pro.fut_basic(exchange='CFFEX')
    fut_basic.to_csv('data/fut_basic.csv', index=False)
    print("股指期货基本信息获取并保存成功")
except Exception as e:
    print(f"获取股指期货基本信息时发生错误: {e}")
