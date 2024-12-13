from django.shortcuts import render, redirect
from loginpage.models import Member
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse


# Create your views here.
def main(request):
  id = request.session['session_id']
  qs = Member.objects.filter(id=id)

  # 생년월일을 8자리 문자열로 받았다 가정
  birth_date = qs[0].birthday

  # 문자열 슬라이싱을 통해 년, 월, 일을 분리하고 점으로 구분
  formatted_birth_date = f"{birth_date[:4]}.{birth_date[4:6]}.{birth_date[6:]}"

  print(formatted_birth_date)  # 결과: 1990.12.31

  context = {'my':qs[0], 'my_birth':formatted_birth_date}
  return render(request, 'mymain.html', context)

def modify(request):
  # 회원 정보 수정 불러오기
  id = request.session['session_id']
  qs = Member.objects.filter(id=id)
  if request.method == 'GET':
    print('get : ',qs[0].nicName)
    email = qs[0].mail.split('@')
    context = {'mem_info':qs[0], 'mail_id':email[0], 'mail_domain':email[1]}
    return render(request, 'mypage_modi.html', context)
  
  # 바뀐 정보 불러오기 및 저장
  else:
    nicName = request.POST.get('mypage_nicname')
    mail_id = request.POST.get('mypage_mailid')
    mail_domain = request.POST.get('mypage_email2')
    gender = request.POST.get('mypage_gender')
    birthday = request.POST.get('mypage_birth')
    print(nicName)

    qs.update(
    nicName = nicName,
    mail = f'{mail_id}@{mail_domain}',
    gender = gender,
    birthday = birthday
    )

    print('post : ',qs[0].nicName)
    return redirect('/mypage/main/')

# 회원정보 수정 > 현재 비밀번호 확인
def currpw_chk(request):
  id = request.session['session_id']
  pw = request.POST.get('currPw','')
  qs = Member.objects.filter(pw=pw, id=id)
  
  if qs:
    context = {'result':'success'}
  else:
    context = {'result':'fail'}
    print('에러')

  return JsonResponse(context) 

# 회원정보 수정 > 비밀번호 변경
def pw_chg(request):
  id = request.session['session_id']
  newPw = request.POST.get('newPw')
  qs = Member.objects.get(id=id)
  print(qs.pw)
  qs.pw = newPw
  qs.save()
  print(qs.pw)
  return JsonResponse({'result': 'success'})


# 회원 탈퇴
def delaccount(request):
  id = request.session['session_id']
  qs = Member.objects.get(id=id)
  qs.delete()
  return redirect('/')