from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

# Create your views here.
# 직접 구현한 함수형 뷰
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     # output = ", ".join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)
#     print(latest_question_list)
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)

# 장고에서 제공하는 제너릭 뷰를 상속한 클래스형 뷰로 대체
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        '''Return 5 question list'''
        return Question.objects.order_by("-pub_date")[:5]


# 직접 구혀한 함수형 뷰
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {"question": question}
#     return render(request, "polls/detail.html", context)

# 장고에서 제공하는 제너릭 뷰를 상속한 클래스형 뷰로 대체
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

# 장고에서 제공하는 제너릭 뷰를 상속한 클래스형 뷰로 대체
class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {"question": question, "error_message": "You didn't select a choice",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

