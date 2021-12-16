import FinanceDataReader as fdr

 # 종목 정보 가져오기
stock_df = fdr.DataReader('199290')
data_set = stock_df[['Open', 'High', 'Low', 'Close']].reset_index()

data_set.loc[data_set['Open'] == 0, 'Close'] = 0

print(data_set.tail(20))