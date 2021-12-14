from django.shortcuts import render
from .__init__ import model
from .services import predict_stock


def find(request):
    if request.method == "POST":
        return render(request, 'index.html')
    else:
        print("GET 입니다")
        return render(request, 'index.html')

def search(request):
    stock_code = request.GET['stock']
    stock_name = request.GET['name']
    print(stock_code, stock_name)
    
    result, data_set = predict_stock(stock_name, stock_code)
    

    return render(request, 'analysis.html')

def patent(request):
    return render(request, 'patent.html')

def patentKeyword(request):
    return render(request, 'patentKeyword.html')