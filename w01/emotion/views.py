from django.shortcuts import render
from loginpage.models import Member

# Create your views here.
def main(request):
  # 프로필 가져오기 
  mem = Member.objects.filter(id = request.session['session_id'])
  

  context = {'mem_info':mem[0]}
  return render(request, 'e_main.html', context)