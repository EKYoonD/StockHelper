from django.shortcuts import render
# from StockWeb.models import Search
# from django.db.models import Q

# Create your views here.
def find(request):
    if request.method == "POST":
        # get parameter
        searchInput = request.POST['search_input']
        print(searchInput)
        # match stockList and search_input
        # seachResult = Search.objects.all().filter(
        #     Q(name__icontains=searchInput),
        #     Q(description__icontains=searchInput)
        # )
        return render(request, 'index.html')
    else:
        print("GET 입니다")
        return render(request, 'index.html')

def search(request):
    return render(request, 'analysis.html')