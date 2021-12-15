from django.urls import path
from . import views

urlpatterns = [
    path('', views.find),
    path('analysis', views.search),
    path('patent', views.patent),
    path('patentTop50', views.patentTop50),
]