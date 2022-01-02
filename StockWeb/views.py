import re
from django.shortcuts import render
from .services import PredictStock, StockInfo
from datetime import datetime
import time
import pandas as pd



def find(request):

    if request.method == "POST":
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def search(request):

    predictStock = PredictStock()
    stockInfo = StockInfo()

    stock_code = request.GET['stock']
    stock_name = request.GET['name']
    print(stock_code, stock_name)

    # ---------------- 해당 주식 종목의 20일치 종가 + 예측값 ------------------------
    pred_stock_dict = predictStock.predict_stock(stock_name, stock_code)

    # ---------------- 해당 주식 기존 정보들 가져오기 ----------------------------
    # 다트에서 주식종목 정보 가져오기
    all_stock_dict = stockInfo.get_stock_info(stock_code)

    # 다트에서 재무제표 가져오기
    unit, sales_revenue, profit, income, xls_url = stockInfo.get_financial_statements(stock_code)

    # 해당 주식 종목의 차트 정보
    data_set_str, stock_start = stockInfo.all_stock_data(stock_code)  # stock_start : 종목 상장일

    print("성공")
    print(sales_revenue, profit, income, xls_url)

    data = {
        # 회사 상세 정보 데이터
        'stock_name' : stock_name,
        'corp_name' : all_stock_dict['corp_name'],
        'stock_code' : stock_code,
        'owner_name' : all_stock_dict['ceo_nm'],
        'company_area' : all_stock_dict['adres'],
        'type_business' : all_stock_dict['type_business'],
        'main_products' : all_stock_dict['main_products'],
        'stock_start_day' : stock_start,
        'stock_settlement_date' : all_stock_dict['acc_mt'],
        'hompage_url' : all_stock_dict['hm_url'],
        'data_set' : data_set_str,  # 주식의 전체 그래프

        # 재무제표 데이터
        'unit' : unit,
        'sales_revenue' : sales_revenue,
        'profit' : profit,
        'income' : income,
        'xls_url' : xls_url,

        # 예측 데이터
        'stock_close_date_list' : pred_stock_dict['stock_close_date_list'],
        'stock_close_price_list' : pred_stock_dict['stock_close_price_list'],
        'start_date' : pred_stock_dict['ds'],
        'end_date' : pred_stock_dict['de'],
        'news_cnt' : pred_stock_dict['news_cnt'],
        'next_day' : pred_stock_dict['next_day'].replace('-', '.'),
        'pred' : pred_stock_dict['pred'],
        'stock_price_diff' : pred_stock_dict['stock_price_diff'],
        'up_down' : pred_stock_dict['up_down']
    }

    return render(request, 'analysis.html', data)

def patent(request):
    kw = request.GET['kw']
    rank = request.GET['rank']
    return render(request, 'patent.html', {'rank':rank, 'kw':kw})

def patentTop50(request):
    return render(request, 'patentTop50.html')