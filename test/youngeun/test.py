import pandas as pd

stockList = pd.read_csv('static/data/stockList_CSV.csv', dtype='str')

print(stockList[stockList['회사명'] == 'S-Oil']['종목코드'].iloc[0] == '010950')