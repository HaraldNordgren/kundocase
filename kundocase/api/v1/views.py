from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from kundocase.forum.models import Question, Answer
from .utils import get_json, put_json


@csrf_exempt
def questions(request, question_id=None):
    if request.method == 'GET':
        return get_json(question_id, Question, Question.objects)

    elif request.method == 'PUT':
        return put_json(question_id, request.body, Question, Question.objects,
                        ['id', 'created', 'answer'])

    return HttpResponse(status=405)


@csrf_exempt
def answers(request, question_id, answer_id=None):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return get_json(answer_id, Answer, question.answer_set)

    elif request.method == 'PUT':
        return put_json(answer_id, request.body, Answer, question.answer_set,
                        ['id', 'created', 'question', 'question_id'], question)

    return HttpResponse(status=405)
