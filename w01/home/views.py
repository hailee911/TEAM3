from django.shortcuts import render, redirect
from loginpage.models import Member
from diary.models import Content
from django.http import JsonResponse,HttpResponse
from django.db.models import Q


# 랜딩페이지
def landing(request):
  return render(request,'landing.html')

def main(request):
  return render(request, 'main.html')

def logout(request):
  request.session.clear()
  response = redirect('/')
  response.delete_cookie('sessionid')  # 세션 쿠키 삭제
  return response

# 검색창
def search(request):
  id = request.session['session_id']
  csearch = request.POST.get("csearch")
  print("csearch : ",csearch)
  member = Member.objects.get(id=id)
  qs = list(Content.objects.filter(Q(member=member,ctitle__contains=csearch)|Q(member=member,ccontent__contains=csearch) ).values())
  print("qs : ",qs)
  context = {"list_qs":qs}
  return JsonResponse(context)
