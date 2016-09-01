from django.shortcuts import render, get_object_or_404
from kundocase.forum.models import Question

def startpage(request):
    questions = Question.objects.all().order_by("-created")
    return render(request, "forum/startpage.html", {
        "questions": questions,
    })

def question(request, id):
    question = get_object_or_404(Question, id=id)
    answers = question.answer_set.all().order_by("-created")
    return render(request, "forum/question.html", {
        "question": question,
        "answers": answers,
    })
