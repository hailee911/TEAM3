from django.urls import path,include
from . import views

app_name = "comment"
urlpatterns = [
    path('test/', views.test, name="test"),
]
