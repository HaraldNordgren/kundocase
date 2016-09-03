from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from kundocase.forum.models import Question, Answer
from kundocase.forum.forms import QuestionForm, AnswerForm


def startpage(request):
    questions = Question.objects.all().order_by("created")
    return render(request, "forum/startpage.html", {
        "questions": questions,
    })


def add_question(request):
    if request.method == 'GET':
        form = QuestionForm()

    elif request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")

    return render(request, 'forum/add_question.html', {'form': form})


def question(request, question_id, answer_id=None):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answer_set.all().order_by("created")
    editing_mode = False

    if request.method == 'GET':
        if answer_id:
            answer = get_object_or_404(question.answer_set, id=answer_id)
            form = AnswerForm(instance=answer)
            editing_mode = True
        else:
            form = AnswerForm()

    elif request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            if answer_id:
                question.answer_set.filter(id=answer_id).update(**form.cleaned_data)
            else:
                answer = form.save(commit=False)
                answer.question = question
                answer.save()
            form = AnswerForm()

    return render(request, "forum/question.html", {
        "question": question,
        "answers": answers,
        "form": form,
        "editing_mode": editing_mode
    })
