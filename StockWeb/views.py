from django.shortcuts import render
from .services import PredictStock


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
    # print(result)
    # print(data_set)

    print("성공")


    return render(request, 'analysis.html')

def patent(request):
    kw = request.GET['kw']
    return render(request, 'patent.html', {'kw':kw})

def patentKeyword(request):
    return render(request, 'patentKeyword.html')