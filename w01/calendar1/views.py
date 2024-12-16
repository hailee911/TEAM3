from django.shortcuts import render, redirect
from calendar1.models import Event
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from loginpage.models import Member

@csrf_exempt
def update_event(request):
  if request.method == 'POST':
    event_id = request.POST.get('event_id')
    title = request.POST.get('title')
    color = request.POST.get('color')  # 색상 받아오기
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    location = request.POST.get('location')
    repeat = request.POST.get('repeat')
    memo = request.POST.get('memo')

    try:
      event = Event.objects.get(no=event_id)  # 이벤트 찾기
      event.title = title
      event.color = color  # 색상 수정 (튜플 쉼표 제거)
      event.start_date = start_date
      event.end_date = end_date
      event.location = location
      event.repeat = repeat
      event.memo = memo
      event.save()  # 수정된 내용 저장
      return JsonResponse({'success': True}, status=200)
    except Event.DoesNotExist:
      return JsonResponse({'error': '이벤트를 찾을 수 없습니다.'}, status=404)

  return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

# 모든 이벤트를 JSON 형식으로 반환
def son(request):
  events = Event.objects.all()  # 모든 이벤트 가져오기
  events_data = []
  for event in events:
    events_data.append({
      'id': event.no,
      'title': event.title,
      'color': event.color,
      'start': event.start_date.isoformat(),
      'end': event.end_date.isoformat(),
      'location': event.location,
      'memo': event.memo,
      'repeat': event.repeat,
    })
  return JsonResponse(events_data, safe=False)

# 캘린더 페이지 렌더링 및 이벤트 생성
def cal(request):
  if request.method == "POST":
    title = request.POST.get('title')
    color = request.POST.get('color')  # 색상 받아오기
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    location = request.POST.get('location')
    repeat = request.POST.get('repeat')
    memo = request.POST.get('memo')

    # datetime 형식으로 변환
    start_date = timezone.datetime.fromisoformat(start_date)
    end_date = timezone.datetime.fromisoformat(end_date)

    # 이벤트 생성
    Event.objects.create(
      title=title,
      color=color,  # 색상 저장
      start_date=start_date,
      end_date=end_date,
      location=location,
      repeat=repeat,
      memo=memo,
    )
    return redirect(f'/calendar1/cal/')
  else:
    members = Member.objects.all()
    for member in members:
      # 해당 멤버의 생일 이벤트가 이미 생성되었는지 확인
      event_exists = Event.objects.filter(title=f'{member.name}의 생일', start_date=member.birthday).exists()
      
      if not event_exists:  # 이벤트가 없다면 생성
        Event.objects.create(
          title=f'{member.name}의 생일',  # 이벤트 제목
          color='yellow',  # 색상
          start_date=member.birthday,  # 생일 날짜 (시작)
          end_date=member.birthday,  # 생일 날짜 (끝)
          repeat='yearly'
        )
    return render(request, 'calendar.html')

@csrf_exempt
def delete_event(request):
  if request.method == 'POST':
    event_id = request.POST.get('event_id')

    try:
      event = Event.objects.get(no=event_id)  
      event.delete()
      return JsonResponse({'success': True}, status=200)
    except Event.DoesNotExist:
      return JsonResponse({'error': '이벤트를 찾을 수 없습니다.'}, status=404)

  return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)
