import re
from django.shortcuts import render
from .services import PredictStock, StockInfo
from datetime import datetime
import time
import pandas as pd

predictStock = PredictStock()
stockInfo = StockInfo()

def find(request):

    if request.method == "POST":
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def search(request):
    stock_code = request.GET['stock']
    stock_name = request.GET['name']
    print(stock_code, stock_name)

    # ---------------- 해당 주식 기존 정보들 가져오기 ----------------------------
    # 다트에서 재무제표 가져오기
    sales_revenue, profit, income, xls_url = stockInfo.get_stock_info(stock_code)

    # 해당 주식 종목의 차트 정보
    data_set, stock_start = stockInfo.all_stock_data(stock_code)
    # 날짜 timestamp 형식으로 변경
    data_set['Date'] = data_set['Date'].apply(lambda date: int(time.mktime(date.timetuple())) * 1000)
    print(data_set)
    # 데이터 펼치기
    data_set_list = data_set.values.tolist()
    print(data_set_list)
    data_set_list = [','.join(map(lambda n: str(n), data_list)) for data_list in data_set_list]
    data_set_str = ','.join(data_set_list)

    # ---------------- 해당 주식 종목의 20일치 종가 + 예측값 ------------------------
    result, ds, de, news_cnt = predictStock.predict_stock(stock_name, stock_code)
    result.index = map(lambda date: str(date)[:10], result.index)
    for i in range(21):
        result.iloc[i] = int(result[i])
    
    print('해당 주식 종목의 20일치 종가 + 예측값')    
    stock_close_date_list = list(result.index)  # 날짜
    stock_close_price_list = list(result.values) # 종가
    print(stock_close_date_list)
    print(stock_close_price_list)

    next_day = result.index[-1]
    pred = int(result.iloc[-1])

    print("성공")
    print(sales_revenue, profit, income, xls_url)

    data = {
        'name' : stock_name,
        'sales_revenue' : sales_revenue,
        'profit' : profit,
        'income' : income,
        'xls_url' : xls_url,

        'close_data_set' : result,
        'stock_close_date_list' : stock_close_date_list,
        'stock_close_price_list' : stock_close_price_list,
        'data_set' : data_set_str,
        'ds' : ds,
        'de' : de,
        'news_cnt' : news_cnt,
        'stock_name' : stock_name,
        'next_day' : next_day.replace('-', '.'),
        'pred' : pred,
        'stock_start' : stock_start
    }

    return render(request, 'analysis.html', data)

def patent(request):
    kw = request.GET['kw']
    rank = request.GET['rank']
    return render(request, 'patent.html', {'rank':rank, 'kw':kw})

def patentTop50(request):
    return render(request, 'patentTop50.html')