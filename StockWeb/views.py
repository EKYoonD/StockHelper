from django.shortcuts import render
from .services import PredictStock
from datetime import datetime
import time

predictStock = PredictStock()

def find(request):

    if request.method == "POST":
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def search(request):
    stock_code = request.GET['stock']
    stock_name = request.GET['name']
    print(stock_code, stock_name)
    
    # 해당 주식 종목의 모든 정보
    data_set, stock_start = predictStock.all_stock_data(stock_code)
    # 날짜 timestamp 형식으로 변경
    data_set['Date'] = data_set['Date'].apply(lambda date: int(time.mktime(date.timetuple())) * 1000)
    print(data_set)
    # 데이터 펼치기
    data_set_list = data_set.values.tolist()
    print(data_set_list)
    data_set_list = [','.join(map(lambda n: str(n), data_list)) for data_list in data_set_list]
    data_set_str = ','.join(data_set_list)

    # 해당 주식 종목의 20일치 종가 + 예측값
    result, ds, de, news_cnt = predictStock.predict_stock(stock_name, stock_code)
    result.index = map(lambda date: str(date)[:10], result.index)
    for i in range(21):
        result.iloc[i] = int(result[i])
    print(result)

    next_day = result.index[-1]
    pred = int(result.iloc[-1])

    print("성공")

    data = {
        'name' : stock_name,
        'close_data_set' : result,
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