from django.urls import path,include
from . import views

app_name = "diary"
urlpatterns = [
    path('diaryHome/', views.diaryHome, name="diaryHome"),
    path('MdiaryList/', views.MdiaryList, name="MdiaryList"),
    path('diaryWrite/', views.diaryWrite, name="diaryWrite"),
    path('diaryMake/', views.diaryMake, name="diaryMake"),
    path('diary_view/<int:cno>/', views.diary_view, name="diary_view"),
    path('dmodify/<int:cno>/', views.dmodify, name='dmodify'),  # 글 수정
    path('CdiaryList/', views.CdiaryList, name="CdiaryList"), # 생성한 다이어리 리스트
    path('JdiaryList/', views.JdiaryList, name="JdiaryList") # 생성한 다이어리 리스트
]
