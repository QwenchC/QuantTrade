import os
from jqdatasdk import auth, get_all_securities

# 登录聚宽
auth('your_username', 'your_password')

# 创建 data 文件夹，如果不存在的话
if not os.path.exists('data'):
    os.makedirs('data')

# 获取沪深A股基本信息
stocks = get_all_securities(types=['stock'])

# 剔除退市整理板块和ST板块
stocks_filtered = stocks[(stocks['end_date'] > '2024-01-01') & (~stocks['display_name'].str.contains('ST'))]

# 获取场内基金基本信息
funds = get_all_securities(types=['fund'])

# 获取股指期货基本信息
futures = get_all_securities(types=['futures'])

# 将数据保存到TXT文件
with open('securities_list.txt', 'w', encoding='utf-8') as f:
    f.write("沪深A股（包含科创板，不包含退市整理板块和ST板块）:\n")
    for index, row in stocks_filtered.iterrows():
        f.write(f"{index}: {row['display_name']}\n")
    
    f.write("\n场内基金:\n")
    for index, row in funds.iterrows():
        f.write(f"{index}: {row['display_name']}\n")
    
    f.write("\n股指期货:\n")
    for index, row in futures.iterrows():
        f.write(f"{index}: {row['display_name']}\n")

print("证券列表保存成功")
