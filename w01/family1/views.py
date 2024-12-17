from django.shortcuts import render
from loginpage.models import Member
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def add_member(request):
  # 로그인한 사용자 ID 가져오기
  id = request.session.get('session_id')
  if not id:
    return JsonResponse({'error': '로그인이 필요합니다.'}, status=400)

  # 입력된 멤버 ID 가져오기
  member_id = request.POST.get('member_id')
  if not member_id:
    return JsonResponse({'error': '멤버 ID를 입력하세요.'}, status=400)

  try:
    # 멤버 찾기
    member = get_object_or_404(Member, id=member_id)

    # 현재 로그인한 사용자의 created_group 가져오기
    user = Member.objects.get(id=id)
    created_group = user.created_group

    # 멤버가 이미 joined_group을 가지고 있는지 확인
    if member.joined_group is None:
      # joined_group이 None일 경우에만 추가
      member.joined_group = created_group
      member.save()
      return JsonResponse({'success': '멤버가 추가되었습니다.'})
    else:
      # 이미 joined_group이 존재할 경우
      return JsonResponse({'error': '이미 다른 그룹에 속해 있습니다.'})

  except Member.DoesNotExist:
    return JsonResponse({'error': '멤버를 찾을 수 없습니다.'}, status=404)



def delete_member(request, member_id):
    # 현재 로그인한 사용자 ID 가져오기
    id = request.session.get('session_id')
    if not id:
        return JsonResponse({'error': '로그인이 필요합니다.'}, status=400)

    try:
        # 삭제할 멤버 찾기
        member = get_object_or_404(Member, id=member_id)
        
        # 현재 사용자가 삭제할 멤버의 그룹에 속해 있는지 확인
        if member.joined_group:
            # joined_group을 빈 값으로 설정
            member.joined_group = None
            member.save()
            return JsonResponse({'success': '멤버가 삭제되었습니다.'})
        else:
            return JsonResponse({'error': '삭제할 멤버의 그룹 정보가 없습니다.'}, status=400)

    except Member.DoesNotExist:
        return JsonResponse({'error': '멤버를 찾을 수 없습니다.'}, status=404)



def fam(request):
    # 현재 로그인한 사용자 ID 가져오기
    id = request.session.get('session_id')
    if not id:
        return render(request, 'login.html', {'error': '로그인이 필요합니다.'})
    
    try:
        # 사용자 정보 가져오기
        user = Member.objects.get(id=id)
    except Member.DoesNotExist:
        return render(request, 'fam.html', {'error': '사용자를 찾을 수 없습니다.'})

    # 생성된 그룹과 가입된 그룹 가져오기
    created_group = user.created_group or ''
    joined_group = user.joined_group or ''
    
    # 쉼표로 분리하여 리스트로 변환
    created_group_list = list(str(created_group).split(','))
    joined_group_list = list(str(joined_group).split(','))

    # 리스트 길이 확인 후 안전하게 요소 가져오기
    created_group_name = created_group_list[2] if len(created_group_list) > 2 else None
    joined_group_name = joined_group_list[2] if len(joined_group_list) > 2 else None

    # 같은 그룹에 가입된 멤버들 가져오기
    joined_group_members = Member.objects.filter(joined_group=created_group) if created_group else []
    if not joined_group_members:user.created_group = None
    if not joined_group_members:created_group = None

    # 같은 그룹에 가입된 멤버들 가져오기2
    created_group_members = Member.objects.filter(Q(created_group=joined_group) | Q(joined_group=joined_group)).exclude(id=id) if joined_group else []
    created_group_members1 = Member.objects.filter(created_group=joined_group) if joined_group else []
    if not created_group_members1:user.joined_group = None
    if not created_group_members1:joined_group = None
    user.save()

    # 그룹 존재 여부 확인
    has_group = bool(created_group or joined_group)

    # 컨텍스트 데이터 구성
    context = {
        'user':user,
        'has_group': has_group,
        'created_group': created_group,
        'joined_group': joined_group,
        'created_group_name': created_group_name,
        'joined_group_name': joined_group_name,
        'joined_group_members': joined_group_members,
        'created_group_members': created_group_members,
    }

    return render(request, 'fam.html', context)