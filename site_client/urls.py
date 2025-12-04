from django.urls import path 
from site_client import views 

urlpatterns = [
    path('', views.index, name='index'),
]
