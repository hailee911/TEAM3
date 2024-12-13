from django.shortcuts import render,redirect
from calendar1.models import Event
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.utils import timezone


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
            event.color = color,  # 색상 저장
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



# json
def son(request):
  events = Event.objects.all()  # 모든 이벤트 가져오기
  events_data = []
  for event in events:
    events_data.append({
      'id' : event.no,
      'title': event.title,
      'color': event.color,
      'start': event.start_date.isoformat(),
      'end': event.end_date.isoformat(),
      'location': event.location,
      'memo': event.memo,
      'repeat': event.repeat,
    })
  return JsonResponse(events_data, safe=False)

# 캘린더
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
      color = color,  # 색상 저장
      start_date=start_date,
      end_date=end_date,
      location=location,
      repeat=repeat,
      memo=memo,
    )
    user_id = request.POST.get('user_id') 
    return redirect(f'/calendar1/cal/?user_id={user_id}')
  else:
    user_id = request.GET.get('user_id') 
    context = {'user_id':user_id}
    return render(request, 'calendar.html',context)

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
