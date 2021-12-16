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

    # ---------------- 해당 주식 기존 정보들 가져오기 ----------------------------
    # 다트에서 주식종목 정보 가져오기
    stock_dict = stockInfo.get_stock_info(stock_code)

    # 다트에서 재무제표 가져오기
    sales_revenue, profit, income, xls_url = stockInfo.get_financial_statements(stock_code)

    # 해당 주식 종목의 차트 정보
    data_set_str, stock_start = stockInfo.all_stock_data(stock_code)  # stock_start : 종목 상장일

    print("성공")
    print(sales_revenue, profit, income, xls_url)

    data = {
        'stock_name' : stock_name,
        'corp_name' : stock_dict['corp_name'],
        'stock_code' : stock_code,
        'owner_name' : stock_dict['ceo_nm'],
        'company_area' : stock_dict['adres'],
        'type_business' : stock_dict['type_business'],
        'main_products' : stock_dict['main_products'],
        'stock_start_day' : stock_start,
        'stock_settlement_date' : stock_dict['acc_mt'],
        'hompage_url' : stock_dict['hm_url'],

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