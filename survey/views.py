import survey
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from survey.models import Survey, Answer

# Create your views here.


def main(request):
    # filter => where
    # order_by("필드") 오름차순, order_by("-필드") 내림차순
    # select * from servey_servey where status='y'
    # order_by survey_idx desc limted 1
    survey = Survey.objects.filter(status='y').order_by("-survey_idx")[0]

    # main.html페이지로 이동, 데이터 전달
    return render(request, "main.html", {'survey': survey})


def show_result(request):
    idx = request.GET["survey_idx"]
    ans = Survey.objects.get(survey_idx=idx)
    answer = [ans.ans1, ans.ans2, ans.ans3, ans.ans4]
    surveyList = Survey.objects.raw("""
        select
            survey_idx, num, count(num) sum_num,
            round((select count(*) from survey_answer
                where survey_idx=a.survey_idx and num=a.num)*100.0 /
                (select count(*) from survey_answer
                    where survey_idx=a.survey_idx),1) rate
        from survey_answer a
        where survey_idx=%s
    group by survey_idx, num
    order by num
    """, idx)
    surveyList = zip(surveyList, answer)
    print("surveyList:", surveyList)
    print("answer:", answer)

    # select count(*) from survey_answer
    count = Answer.objects.all().count()

    return render(request, 'result.html', {'surveyList': surveyList, "count": count})


@csrf_exempt
def save_survey(request):
    # survey_idx : 설문 문항 코드
    # num : 사용자가 선택한 번호
    dto = Answer(
        survey_idx=request.POST["survey_idx"], num=request.POST["num"])
    dto.save()  # insert쿼리 실행
    # 성공화면 success.html로 이동
    return render(request, 'success.html')
