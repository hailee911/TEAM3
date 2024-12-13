from django.shortcuts import render
from loginpage.models import Member

def fam(request):
  # 현재 로그인한 사용자 가져오기
  id = request.session['session_id']
  user = Member.objects.get(id=id)  # 가정: request.user가 Member 모델 객체임
  print("맴버:",user)
  created_group:
  created_group = user.created_group
  joined_group = user.joined_group
  has_group = user.created_group or user.joined_group
  # 쉼표로 구분된 값을 분리하여 리스트로 만들기
  created_group_list = list(str(created_group).split(','))
  joined_group_list = list(str(joined_group).split(','))

  # 두 번째 항목 가져오기 (인덱스 1)
  created_group_name = created_group_list[2]  # 인덱스는 0부터 시작하므로 두 번째 항목은 인덱스 1
  joined_group_name = joined_group_list[2]  # 인덱스는 0부터 시작하므로 두 번째 항목은 인덱스 1
  print("가족제목 : ",created_group_name)
  context = {
      'created_group': created_group,  # 그룹이 있는지 여부
      'has_group': has_group,  # 그룹이 있는지 여부
      'joined_group': joined_group,  # 그룹이 있는지 여부
      'created_group_name':created_group_name,
      'joined_group_name':joined_group_name
  }
  return render(request, 'fam.html', context)