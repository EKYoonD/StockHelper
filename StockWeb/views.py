from django.shortcuts import render

# Create your views here.
def find(request):
    return render(request, 'index.html')

def search(request):
    return render(request, 'analysis.html')