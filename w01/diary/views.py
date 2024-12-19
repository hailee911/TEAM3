from django.shortcuts import render, redirect
from loginpage.models import Member
from diary.models import Letter
from django.utils import timezone
from diary.models import Content
from diary.models import GroupDiary
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Max
from django.db.models import Q



# 우체통
from .models import MdiaryBoard

## 다이어리 HOME
def diaryHome(request):
  id = request.session.get('session_id')
  name = request.session.get('session_name')
  qs_group = GroupDiary.objects.filter(member=id)

  ## 공유 일기장
  # 1. 유저가 생성공유일기장

  qs_createdDiary = GroupDiary.objects.filter(Q(member__id=id) & Q(role=1))
  c_context = {} #변수

  if qs_createdDiary:
    # 초대멤버가져오기
    qs_joinedMem = GroupDiary.objects.filter(gno=qs_createdDiary[0].gno, role=2)
    if qs_joinedMem:
      c_context = {"creator":qs_createdDiary[0], "user_name":name, "joined_members":qs_joinedMem}
      print("있음",c_context)
    else:
      c_context = {"creator":qs_createdDiary[0], "user_name":name,}
      print("없음",c_context)
  

  # 2. 유저가 가입한 공유일기장
  qs_joinedDiary = GroupDiary.objects.filter(Q(member__id=id) & Q(role=2))
  if qs_joinedDiary:
    # 멤버 정보가져오기
    # 방장
    gno = qs_joinedDiary[0].gno
    qs_cMem = Member.objects.filter(created_group__gno=gno).first()

    jmems = []
    for jmem in qs_joinedDiary:
      member = jmem.member
      j = Member.objects.get(id=member.id)
      jmems.append(j.name)
    c_context['cMem'] = qs_cMem
    c_context['join_d'] = list(qs_joinedDiary)
    c_context['joined_names'] = jmems


  ## 개인 다이어리
  qs_pDiary = MdiaryBoard.objects.get(id=id)
  c_context['pDiary'] = qs_pDiary


  c_context['group'] = qs_group
  print("c_context : ",c_context)
  return render(request,'diaryHome.html',c_context)




  # 우체통
  qs = Letter.objects.all().order_by("ldate")
  member = Member.objects.filter(id=id)
  # personal_diaries = MdiaryBoard.objects.select_related('id').all() # 개인 다이어리 데이터 가져오기
  if member:
    user_nic = member[0].nicName
    context = {"list":qs ,'user_nic':user_nic}
    return render(request,'diaryHome.html',context)
  else:
    context = {'list':qs}
    return render(request,'diaryHome.html',context)
  



## 가족다이어리 생성
def diaryMake(request):
  if request.method == 'GET':
    qs_Member = Member.objects.all()
    id = request.session['session_id']
    qs_createdDiary = GroupDiary.objects.filter(Q(member__id=id) & Q(role=1))
    if qs_createdDiary:
      context = {"gmsg":"0"}
      return render(request,'diaryHome.html', context)
    else:
      context = {'members':qs_Member,"gmsg":"1"}
      return render(request,'diaryMake.html', context)

  else:

    id = request.session['session_id']
    member = Member.objects.get(id=id)
    gtitle = request.POST.get('gtitle')
    gName = request.POST.get('gName')
    created_at = request.POST.get('created_at','')
    search_members = request.POST.getlist('search_members[]')
    
    # GroupDiary에 방장 저장
    qs_creator = GroupDiary.objects.create(gtitle=gtitle, gName=gName, created_at=created_at, member=member)
    no = GroupDiary.objects.aggregate(max_gno = Max('gno'))
    qs_creator.gno = no['max_gno']+1
    qs_creator.role = 1
    qs_creator.save()
    
    # Member에 created_group에 방장 저장
    qs_cMem = Member.objects.get(id=id)
    qs_cMem.created_group = qs_creator
    qs_cMem.save()

    # 초대 멤버 저장
    for sMem in search_members:
      # GroupDiary에 멤버 저장
      gno = qs_creator.gno
      role = 2
      qs_sMem = Member.objects.get(id=sMem)
      qs_joinedMem = GroupDiary.objects.create(gno=gno, gtitle=gtitle, gName=gName, created_at=created_at, member=qs_sMem, role=role)

      # Member에 joined_group에 멤버 저장
      qs_sMem.joined_group = qs_joinedMem
      qs_sMem.save()
    
    context = {"gmsg":"1"}

    return render(request, 'diaryHome.html', context)
  




## 내 다이어리 목록
# def MdiaryList(request):
#   qs = Content.objects.all().order_by("-cdate")
#   context = {'content':qs}  
#   return render(request,'MdiaryList.html', context)


def MdiaryList(request):
  if request.method == "GET":        
    # 세션에 저장된 ID 가져오기
    session_id = request.session.get('session_id')  # 세션에서 'session_id'를 가져옴
    print("세션아이디:", session_id)

    # 세션에 해당하는 ID가 존재하는지 확인
    if not session_id:
      return render(request, 'error.html', {'message': '세션 ID가 존재하지 않습니다.'})
    
    # session_id를 기준으로 Member 찾기
    member = Member.objects.filter(id=session_id).first()

    # member가 없으면 에러 처리
    if not member:
      return render(request, 'error.html', {'message': '사용자 정보가 존재하지 않습니다.'})

    # MdiaryBoard와 Content 가져오기
    mdiary = MdiaryBoard.objects.filter(id=member).first()  # 사용자와 연결된 MdiaryBoard
    if not mdiary:
      return render(request, 'error.html', {'message': '다이어리 정보가 없습니다.'})

    # 해당 멤버의 Content 가져오기
    qs = Content.objects.filter(member=member).select_related('mdiary').order_by("-cdate")

    npage = request.GET.get('npage', 1)
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(npage)
    
    context = {'content': page_obj.object_list,'MdiaryList':page_obj,'mdiary':mdiary}
    return render(request, 'MdiaryList.html', context)
  
  # npage = int(request.GET.get('npage',1))  # 넘어온 현재페이지
  # qs = Content.objects.all().order_by("-cno")
  # # 하단페이지 처리(넘버링)
  # paginator = Paginator(qs,10)  # 10개로 분할
  # mlist = paginator.get_page(npage)  # 1페이지 10개
  # context = {"MdiaryList":mlist, "npage":npage}
  # return render(request,'MdiaryList.html',context)

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import Member, Content

# create 일기장 보기
def CdiaryList(request):
    if request.method == "GET":
        id = request.session.get('session_id')  # 현재 사용자의 ID 가져오기

        # 현재 로그인한 사용자 확인
        member = Member.objects.filter(id=id).first()
        if not member:
            return HttpResponse("사용자 정보가 존재하지 않습니다.", status=400)

        # 사용자가 만든 그룹 (created_group) 정보
        created_group = member.created_group

        # 사용자가 초대된 그룹 (joined_group) 정보
        joined_group = member.joined_group

        # 사용자가 속한 그룹에 해당하는 모든 게시글 가져오기
        if created_group or joined_group:
            # 자신이 속한 그룹에 공유된 게시글 가져오기
            diaries = Content.objects.filter(
                Q(group_diary=created_group) | Q(group_diary=joined_group),  # 그룹 다이어리 기준으로
                group_diary__isnull=False  # group_diary가 None이 아닌 게시글만
            ).order_by('-cdate')  # 최신순 정렬
        else:
            diaries = Content.objects.none()  # 그룹에 속하지 않으면 게시글 없음

        return render(request, 'CdiaryList.html', {
            'diaries': diaries,            # 다이어리 리스트
            'created_group': created_group  # 그룹 정보
        })

## join 일기장 보기
def JdiaryList(request):
      if request.method == "GET":
        # 세션에 저장된 ID 가져오기
        session_id = request.session.get('session_id')  # 세션에서 'session_id'를 가져옴
        print("세션아이디:", session_id)
        # session_id를 기준으로 Member 찾기
        member = Member.objects.filter(id=session_id).first()
        if member.joined_group:
          # Member 에서 join 다이어리 gno 가져오기
          gno = member.joined_group.gno
          joingroup = GroupDiary.objects.filter(gno=gno).first()
          print('조인된 그룹 : ',joingroup)
          print('조인된 그룹 : ',joingroup.created_at)
          # join다이어리의 Content 가져오기
          contents = joingroup.content_set.all().order_by("-cdate")  # 해당 GroupDiary에 연결된 모든 Content 객체 가져오기
          print(contents[0].ctitle)
          if not contents:
            return render(request, 'JdiaryList.html')
          npage = request.GET.get('npage', 1)
          paginator = Paginator(contents, 10)
          page_obj = paginator.get_page(npage)
          context = {
            'member':member,
            'content': page_obj.object_list,
            'JdiaryList':page_obj,
            'jdiary':contents,
            'joinDiary':joingroup }
          return render(request, 'JdiaryList.html', context)

        else:
          return render(request, 'JdiaryList.html')




# 다이어리 작성 저장
def diaryWrite(request):
  if request.method == "GET":
    # 세션에서 사용자 ID 가져오기
    id = request.session.get('session_id')  # 현재 사용자의 ID 가져오기
    current_date = timezone.now().date().strftime('%Y-%m-%d')
    # 생성한 그룹과 참여한 그룹 가져오기
    user = Member.objects.filter(id=id)
    created_group = user[0].created_group
    joined_group = user[0].joined_group
    return render(request, 'diaryWrite.html', {
      'current_date': current_date,
      'created_group': created_group,
      'joined_group': joined_group,
    })
  elif request.method == "POST":
    current_date = timezone.now().date().strftime('%Y-%m-%d')
    # 세션에서 사용자 ID 가져오기
    id = request.session.get('session_id')  # 세션에서 사용자 ID 가져오기
    if not id:
      return HttpResponse("로그인 정보가 없습니다.", status=400)
    # Member 모델에서 해당 ID로 회원 조회
    member = Member.objects.filter(id=id).first()  # 없으면 None 반환
    if not member:
      return HttpResponse("사용자 정보가 존재하지 않습니다.", status=400)
    # 다이어리 작성 내용 저장
    title = request.POST.get('title')
    content = request.POST.get('content')
    image = request.FILES.get('image')
    diary_idc = request.POST.get('diary_idc','')
    diary_idj = request.POST.get('diary_idj','')
    selected_groups = [diary_idc,diary_idj]
    date = request.POST.get('date')
    if date != current_date:
      cdate = date
    else:
      cdate = timezone.now()
    # 로그인 후 첫 접속 시 세션에 diary_count 초기화 (새로운 세션 시작)
    if f"diary_count_{id}" not in request.session:
      request.session[f"diary_count_{id}"] = 1
    else:
      # 세션에 diary_count가 있으면 증가
      diary_count = request.session[f"diary_count_{id}"] + 1
      request.session[f"diary_count_{id}"] = diary_count
    # cno는 세션 고유 번호로 관리된 카운터 값 사용
    cno = str(request.session[f"diary_count_{id}"])
    # Content 객체 생성하여 저장
    new_diary = Content(
      cno=cno, #생성된 cno사용
      member=member,
      ctitle=title,
      ccontent=content,
      image=image,
      cdate=cdate,
    )
    new_diary.save()
    ## 공유하려는 다이어리가 있으면
    print("selected_groups : ",selected_groups)
    if selected_groups[0]  == '' and  selected_groups[1]  == '':
      return redirect('diary:MdiaryList')
    else:
        # join된 일기장에만 공유
        if selected_groups[0] == '':
            joined_group = GroupDiary.objects.filter(gno=selected_groups[1]).first()
            new_diary.group_diary.add(joined_group)
        # create 한 일기장에만 공유
        elif selected_groups[1] == '':
            created_group = GroupDiary.objects.filter(gno=selected_groups[0]).first()
            new_diary.group_diary.add(created_group)
        # 모두 공유
        else:
            created_group = GroupDiary.objects.filter(gno=selected_groups[0]).first()
            joined_group = GroupDiary.objects.filter(gno=selected_groups[1]).first()
            new_diary.group_diary.add(created_group,joined_group)
        print("그룹다이어리 : ",new_diary.group_diary)
        return redirect('diary:MdiaryList')  # 다이어리 리스트로 리다이렉트
      


# 다이어리 view 추후 업데이트 >>
def diaryView(request):
  id = request.session.get('session_id')
  member = Member.objects.filter(id=id)
  qs = Content.objects.filter(member=member[0])
  context = {"content":qs}
  return render(request,'diary_view.html',context)

# 좋댓
# from .models import Comment, Like


# # 좋아요 처리
# def toggle_like(request, content_id):
#     if request.method == "POST":
#         member_id = request.session.get('session_id')
#         if not member_id:
#             return JsonResponse({"error": "로그인 상태가 아닙니다."}, status=401)

#         member = Member.objects.get(id=member_id)
#         content = Content.objects.get(pk=content_id)

#         # 좋아요 상태 토글
#         like, created = Like.objects.get_or_create(content=content, member=member)
#         if not created:
#             like.delete()
#             liked = False
#         else:
#             liked = True

#         # 좋아요 개수 반환
#         like_count = Like.objects.filter(content=content).count()
#         return JsonResponse({"liked": liked, "like_count": like_count})

# # 댓글 작성
# def add_comment(request, content_id):
#     if request.method == "POST":
#         member_id = request.session.get('session_id')
#         text = request.POST.get("text")

#         if not member_id or not text:
#             return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

#         member = Member.objects.get(id=member_id)
#         content = Content.objects.get(pk=content_id)

#         comment = Comment.objects.create(content=content, member=member, text=text)

#         return JsonResponse({
#             "comment_id": comment.id,
#             "member_name": member.name,
#             "created_at": comment.created_at.strftime("%Y.%m.%d %H:%M:%S"),
#             "text": comment.text,
#         })