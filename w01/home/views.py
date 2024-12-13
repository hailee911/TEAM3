from django.shortcuts import render, redirect
from loginpage.models import Member


# 랜딩페이지
def landing(request):
  return render(request,'landing.html')

def main(request):
  return render(request, 'main.html')

def logout(request):
  request.session.clear()
  return redirect('/')

