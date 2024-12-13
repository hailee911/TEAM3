from django.urls import path
from . import views

app_name="family1"
urlpatterns = [
    path('fam/', views.fam, name='fam'),
]
