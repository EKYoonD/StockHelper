from django.shortcuts import render
from .__init__ import model


def find(request):
    if request.method == "POST":
        return render(request, 'index.html')
    else:
        print("GET 입니다")
        return render(request, 'index.html')

def search(request):
    stock_code = request.GET['stock']
    print(stock_code)
    print(model)

    return render(request, 'analysis.html')

def patent(request):
    return render(request, 'patent.html')