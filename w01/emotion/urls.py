from django.urls import path,include
from . import views

app_name = "emotion"
urlpatterns = [
    path('main/', views.main, name="main"),
    path('main_data1/', views.main_data1, name="main_data1"),
    path('main_data2/', views.main_data2, name="main_data2"),
    path('main_data4/', views.main_data4, name="main_data4"),
]
