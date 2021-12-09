from django.shortcuts import render
from .__init__ import model


def find(request):
    if request.method == "POST":
        return render(request, 'index.html')
    else:
        print("GET 입니다")
        return render(request, 'index.html')

def search(request):
    return render(request, 'analysis.html')