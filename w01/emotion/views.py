from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models import Sum, Count, F
from django.db.models.functions import Extract, TruncDate
from math import ceil
from calendar import monthrange
from loginpage.models import Member
from emotion.models import EmotionScore

# AI PYTHON
import os
import base64
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import vertexai

# AI 작업을 위한 별도 함수 정의
def generate_for_multiple_files(mbti):
    model = GenerativeModel("gemini-1.5-flash-002")
    for i in range(1, 8):  # 처리할 파일 범위
        input_file_path = f"emotion/gemini/d{i}.txt"
        # output_file_path = f"emotion/gemini/r{i}.txt"
        # 현재 날짜를 파일 이름에 추가 (예: r2024-12-16.txt)
        current_date = datetime.now().strftime("%Y-%m-%d")
        output_file_path = f"emotion/gemini/r{current_date}_{i}.txt"
        
        try:
            with open(input_file_path, "r", encoding="utf-8") as file:
                file_content = file.read()
        except FileNotFoundError:
            continue

        # 유저 MBTI
        # MBTI = "ENTJ"
        
        combined_content = f"{file_content}\\n\\nMBTI: {mbti}"
        encoded_content = base64.b64encode(combined_content.encode("utf-8")).decode("utf-8")
        document = Part.from_data(mime_type="text/plain", data=encoded_content)
        
        text1 = """오늘 느낀 감정의 정리: Identify the overall sentiment of the review (e.g., positive, negative, or neutral).

        설명: Provide a detailed explanation and analysis for the identified sentiment, written in Korean. Make it sound like a psychologist's analysis. Do not write the explanation about MBTI and LBTI in here, write them
        in the MBTI/LBTI section.

        MBTI/LBTI AI 예측: The explanation must include references to the content of the review while retaining the words \"MBTI\" and \"LBTI\" in English. There should be no English words in the explanation.
        Predict the user's likely MBTI and LBTI types based on the review content. These predictions should be made confidently and articulated like a psychologist's analysis. Do not include statements like \"it is difficult to predict\" or \"requires more information.\"
        There's going to be a MBTI provided in the review from the user which is what they got for their MBTI prediction from the MBTI Test. 
        Compare them with the user's MBTI. If the content based "predicted by AI" MBTI is somewhat different with the user's MBTI, quote which part is different.
        It gives the user more interest if the MBTI is different say which MBTI suits the user in the journal.(very important)

        감정 점수: Calculate and present the percentages on the level of joy(기쁨의 정도), anxiety and stress(불안감과 스트레스), social satisfaction(사회적 만족감), achievement and self-esteem(성취와 자존감), and physical/mental well-being(신체적/정신적 웰빙).
        Ensure each emotion's total equals 100% and based on the scores, include the score of happiness(행복도 점수). Do not change the name. 행복도 점수는 100점 만점. 무조건.
        When scoring the happiness be very critical consider on the MBTI understand how this person will actually be happy or not. Do not say them directly but show them in the score. 

        동기부여 메세지: Conclude with an uplifting quote to motivate the user and encourage them to keep writing journals for further updates. No English. Write down a wise saying.

        The output should begin with \"스마트 AI 감정 분석 진단\" and be written in an engaging, detailed manner for better understanding and interest. Maintain a clear structure and avoid unnecessary complexity.
        Organize the analysis results with a specific date format (YYYY-MM-DD-Day) at the start of the analisis after the title.
        Lastly this report will be saved as .txt file so divide the sentences to look pretty and readable also section's name should be equal everytime.
        DO NOT CHANGE THE SECTIONS.
        """
        
        generation_config = {"max_output_tokens": 3333, "temperature": 1, "top_p": 0.95}
        safety_settings = [
            SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=SafetySetting.HarmBlockThreshold.OFF)
        ]
        
        responses = model.generate_content([document, text1], generation_config=generation_config, safety_settings=safety_settings, stream=True)
        output_content = "".join(response.text for response in responses)
        
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(output_content)

# AI 작업을 위한 뷰 함수
def run_ai_process(request):
    if request.method == 'GET':
        # 사용자가 선택한 MBTI 값 가져오기
        selected_mbti = request.GET.get('mbti')
    
    # Google Vertex AI 설정
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
    vertexai.init(project="alert-condition-443702-g2", location="us-central1")
    
    # AI 작업 실행
    generate_for_multiple_files(selected_mbti)

    # # 생성된 파일 내용 반환 (예: r1.txt)
    # output_file_path = "emotion/gemini/r1.txt"
    # if os.path.exists(output_file_path):
    #     with open(output_file_path, "r", encoding="utf-8") as f:
    #         content = f.read()
    #     return render(request, 'report.html', {'content': content})  # 템플릿에 데이터 전달
    # else:
    #     return render(request, 'report.html', {'error': '파일이 생성되지 않았습니다.'})  # 오류 처리

    # 생성된 파일들 읽어서 내용 이어서 출력
    output_content = ""
    
    for i in range(1, 8):  # r1.txt, r2.txt, r3.txt 순으로 파일 읽기
        # output_file_path = f"emotion/gemini/r{i}.txt"
        current_date = datetime.now().strftime("%Y-%m-%d")  # 파일 이름의 날짜 부분
        output_file_path = f"emotion/gemini/r{current_date}_{i}.txt"
        
        if os.path.exists(output_file_path):
            with open(output_file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
                # output_content += f"--- 일기{i}.txt ---\n"  # 각 파일 구분 라인
                output_content += f"--- {current_date} 일기 (마지막으로 수정된 날 기준입니다.) ---\n"  # 각 파일 구분 라인
                output_content += file_content + "\n\n"  # 파일 내용 추가
        else:
            output_content += f"이번 주 일기{i} 생성되지 않았습니다.\n\n"  # 파일 없을 때 메시지 추가
            
            
    # 정상적으로 결과가 있으면 render를 호출하여 페이지 반환
    return render(request, 'report.html', {'content': output_content})

def report(request):
    return render(request, 'report.html')


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

  # emotionscore 가져오기
  file_path = r'C:\Users\KOSMO\Documents\GitHub\TEAM3\w01\media\txt\r2024-12-16_5.txt'  # 파일 경로

  with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()  # 파일의 모든 줄을 리스트로 읽기
    target_keyword = "행복 점수"
    filtered_lines = [line.strip() for line in lines if target_keyword in line]
    print(filtered_lines)

    import re
    data = []
    for line in filtered_lines:
        matches = re.findall(r'\d+', line)  # 정규식으로 숫자만 추출
        data.extend(matches)

    print(data)


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

def main_data5(request):
  # 현재 날짜 기준으로 year, month 구하기
  current_date = datetime.today()
  year = current_date.year
  month = current_date.month
  
  # 4개월 전 날짜 계산
  four_months_ago = current_date.replace(month=current_date.month - 4 if current_date.month > 4 else current_date.month + 8, 
                                             year=current_date.year - 1 if current_date.month <= 4 else current_date.year)
    
  # 프로필 가져오기
  id = Member.objects.get(id = request.session['session_id'])
  member = EmotionScore.objects.filter(member=id)
    
  # 4개월 전부터 현재 월까지의 데이터 구하기
  data = []
  for i in range(4):  # 최근 4개월
    target_month = current_date.month - i
    target_year = current_date.year

    if target_month <= 0:
      target_month += 12
      target_year -= 1
        
    # 해당 월의 첫날과 마지막 날 계산
    first_day_of_month = datetime(target_year, target_month, 1)
    last_day_of_month = datetime(target_year, target_month, monthrange(target_year, target_month)[1])

    # 해당 월에 작성된 일기 수 구하기
    diary_count = EmotionScore.objects.filter(
        member=id,
        diarydate__gte=first_day_of_month,
        diarydate__lte=last_day_of_month
    ).count()

    if diary_count == 0:
        diary_count = 0

    # data에 월과 일기 수 추가
    data.append({
        "name": f"{target_month}월",  # name에 월을 넣음
        "value": diary_count         # value에 해당 월의 일기 수
    })

    print(data)
    # 결과를 JSON 형태로 반환
    return JsonResponse(data, safe=False)