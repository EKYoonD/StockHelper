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
    
    result, data_set = predictStock.predict_stock(stock_name, stock_code)
    data_set = data_set[['Open', 'High', 'Low', 'Close']].reset_index()
    data_set['Date'] = data_set['Date'].apply(lambda date: int(time.mktime(date.timetuple())) * 1000)
    print(data_set)
    data_set_list = data_set.values.tolist()
    print(data_set_list)
    data_set_list = [','.join(map(lambda n: str(n), data_list)) for data_list in data_set_list]
    data_set_str = ','.join(data_set_list)
    # data_set['Date'] = data_set['Date'].apply(lambda date : date.microsecond)
    print(result)

    print("성공")

    data = {
        'name' : stock_name,
        'close_data_set' : result,
        'data_set' : data_set_str
    }

    return render(request, 'analysis.html', data)

def patent(request):
    kw = request.GET['kw']
    return render(request, 'patent.html', {'kw':kw})

def patentKeyword(request):
    return render(request, 'patentKeyword.html')