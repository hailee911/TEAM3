from django.urls import path,include
from . import views

app_name = "emotion"
urlpatterns = [
    path('main/', views.main, name="main"),
]
