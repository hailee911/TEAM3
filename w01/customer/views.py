from django.shortcuts import render
from customer.models import NoticeBoard
from loginpage.models import Member

# Create your views here.
def main(request):
  # 프로필 가져오기 
  mem = Member.objects.filter(id = request.session['session_id'])

  qs = NoticeBoard.objects.order_by('-bno')[:5]
  context = {'notice_5':qs, 'mem_info':mem[0]}
  return render(request, 'customer_service.html', context)

def noticelist(request):
  # 프로필 가져오기 
  mem = Member.objects.filter(id = request.session['session_id'])
  qs = NoticeBoard.objects.all().order_by('-bno')
  context = {'notice_list':qs, 'mem_info':mem[0]}
  return render(request, 'customer_notice_list.html', context)

def noticeview(request, bno):
  # 프로필 가져오기 
  mem = Member.objects.filter(id = request.session['session_id'])
  qs = NoticeBoard.objects.get(bno=bno)
  context = {'view':qs, 'mem_info':mem[0]}
  return render(request, 'customer_notice_view.html', context)