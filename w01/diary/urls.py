from django.urls import path,include
from . import views

app_name = "diary"
urlpatterns = [
    path('diaryHome/', views.diaryHome, name="diaryHome"),
    path('MdiaryList/', views.MdiaryList, name="MdiaryList"),
    path('JdiaryList/', views.JdiaryList, name="JdiaryList"),
    path('CdiaryList/', views.CdiaryList, name="CdiaryList"),
    path('diaryWrite/', views.diaryWrite, name="diaryWrite"),
    path('diaryMake/', views.diaryMake, name="diaryMake"),
    path('diaryView/', views.diaryView, name="diaryView"),
    path('update-title/', views.update_diary_title, name='update_diary_title'),
]
