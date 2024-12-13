from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models import Sum, Count, F
from django.db.models.functions import Extract, TruncDate
from math import ceil
from loginpage.models import Member
from emotion.models import EmotionScore


# Create your views here.
def main(request):
  # 프로필 가져오기 
  mem = Member.objects.filter(id = request.session['session_id'])
  
  # 날짜 가져오기
  current_date = datetime.today()
  year = current_date.year
  month = current_date.month

  # 주 수 가져오기
  # 현재 날짜가 속한 달의 첫 번째 날 (12월 1일)
  first_day_of_month = current_date.replace(day=1)
  # 오늘 날짜와 첫 번째 날 사이의 일수를 계산
  days_into_month = (current_date - first_day_of_month).days

  # 주 수 계산
  week_number = (days_into_month // 7) + 1

  context = {'mem_info':mem[0], 'year':year, 'month':month, 'week':week_number}
  return render(request, 'e_main.html', context)

def main_data1(request):
  # 현재 날짜 기준으로 year, month 구하기
  current_date = datetime.today()
  year = current_date.year
  month = current_date.month

  # 프로필 가져오기 
  id = Member.objects.get(id = request.session['session_id'])
  scores = EmotionScore.objects.filter(member=id, diarydate__year=year, diarydate__month=month)

  # 주 계산 및 평균 값 계산
  grouped_data = (
        scores.annotate(
            day_of_month=Extract('diarydate', 'day'),  # 일(day)만 추출
        )
        .values('day_of_month')  # 일(day) 기준으로 그룹화
        .annotate(
            total_value=Sum('emotionscore'),  # 합계 계산
            count=Count('emotionscore')  # 개수 계산
        )
        .order_by('day_of_month')  # 날짜 순으로 정렬
    )
  
  data = []
  week_data = {}

  for item in grouped_data:
        # 주 계산: (day_of_month - 1) // 7 + 1
        week_of_month = (item['day_of_month'] - 1) // 7 + 1
        average_value = round(item['total_value'] / item['count'], 2)

        # 주별로 묶기
        if week_of_month not in week_data:
            week_data[week_of_month] = {
                'total_value': 0,
                'count': 0
            }

        # 합산
        week_data[week_of_month]['total_value'] += item['total_value']
        week_data[week_of_month]['count'] += item['count']

  # 주별 평균 계산
  for week, values in week_data.items():
      average_value = round(values['total_value'] / values['count'], 2)
      data.append({"name": f"{week}주", "value": average_value})

  return JsonResponse(data, safe=False)

def main_data2(request):
    try:
        # 현재 날짜 기준으로 year, month, weekday(오늘 요일) 구하기
        current_date = datetime.today()
        year = current_date.year
        month = current_date.month
        weekday = current_date.weekday()  # 월요일은 0, 일요일은 6

        # 오늘 날짜가 속한 주의 월요일과 일요일 구하기
        monday_date = current_date - timedelta(days=weekday)  # 오늘에서 weekday만큼 빼면 월요일
        sunday_date = monday_date + timedelta(days=6)

        # 월요일부터 일요일까지의 날짜 목록 생성
        week_dates = [monday_date + timedelta(days=i) for i in range(7)]

        # 프로필 가져오기
        id = Member.objects.get(id=request.session['session_id'])
        scores = EmotionScore.objects.filter(member=id, diarydate__year=year, diarydate__month=month)

        # 오늘 날짜가 속한 주의 데이터 필터링 (월요일 ~ 일요일)
        scores_in_week = scores.filter(diarydate__gte=monday_date, diarydate__lte=sunday_date)

        # 데이터 일자별로 그룹핑
        grouped_data = (
            scores_in_week.annotate(
                day_of_month=Extract('diarydate', 'day'),  # 일(day)만 추출
            )
            .values('day_of_month')  # 일(day) 기준으로 그룹화
            .annotate(
                total_value=Sum('emotionscore'),  # 합계 계산
                count=Count('emotionscore')  # 개수 계산
            )
            .order_by('day_of_month')  # 날짜 순으로 정렬
        )

        # 날짜별로 데이터 매핑
        grouped_data_dict = {
            item['day_of_month']: {
                "total_value": item['total_value'],
                "count": item['count']
            }
            for item in grouped_data
        }

        # 요일 이름 리스트
        weekdays = ["월", "화", "수", "목", "금", "토", "일"]

        # 결과 처리
        data = []
        for date in week_dates:
            day_of_month = date.day
            weekday_name = weekdays[date.weekday()]  # 0=월, 6=일

            # 데이터가 존재하면 평균 계산, 없으면 0으로 초기화
            if day_of_month in grouped_data_dict:
                total_value = grouped_data_dict[day_of_month]['total_value']
                count = grouped_data_dict[day_of_month]['count']
                average_value = round(total_value / count, 2) if count > 0 else 0
            else:
                average_value = 0

            data.append({
                "name": day_of_month,  # 날짜
                "label": weekday_name,  # 요일
                "value": average_value  # 평균값 (없으면 0)
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        # 예외 처리: 오류 발생 시 JSON 응답으로 오류 메시지 반환
        return JsonResponse({"error": "An unexpected error occurred", "message": str(e)}, status=500)

def main_data4(request):
  # 프로필 가져오기 
  id = Member.objects.get(id = request.session['session_id'])
  scores = EmotionScore.objects.filter(member=id)

  data = [
     { "name": "배현지", "value": 7 },
    { "name": "이다영", "value": 11 },
    { "name": "장서윤", "value": 88 },
    { "name": "정종원", "value": 16 },
  ]
  print('데이터4',data)
  return JsonResponse(data, safe=False)