import json

from django.shortcuts import get_object_or_404
from django.core import serializers
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from kundocase.forum.models import Question, Answer


@csrf_exempt
def questions(request, question_id=None):
    if request.method == 'GET':
        if question_id:
            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                return HttpResponse(status=404)
            raw_data = serializers.serialize('python', [question])[0]
            return JsonResponse(raw_data['fields'])
        else:
            raw_data = serializers.serialize('python', Question.objects.all().order_by("created"))
            actual_data = [question['fields'] for question in raw_data]
            return JsonResponse(actual_data, safe=False)

    elif request.method == 'PUT':
        if question_id:
            return HttpResponse(status=404)

        try:
            data = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest("Request body is incorrect JSON")

        new_question = {}
        for field in Question._meta.get_all_field_names():
            if field in ['id', 'created', 'answer']:
                continue
            if field not in data:
                return HttpResponseBadRequest("Request missing '%s' field" % field)
            if not isinstance(data[field], basestring):
                return HttpResponseBadRequest("Values need to be string type")
            new_question[field] = data[field]

        Question.objects.create(**new_question)
        return HttpResponse(status=200)

    return HttpResponse(status=404)


@csrf_exempt
def answers(request, question_id, answer_id=None):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'GET':
        if answer_id:
            answer = get_object_or_404(question.answer_set, id=answer_id)
            raw_data = serializers.serialize('python', [answer])[0]
            return JsonResponse(raw_data['fields'])
        else:
            answers = question.answer_set.all().order_by("created")
            raw_data = serializers.serialize('python', answers)
            actual_data = [answer['fields'] for answer in raw_data]
            return JsonResponse(actual_data, safe=False)

    elif request.method == 'PUT':
        if answer_id:
            return HttpResponse(status=404)
        data = json.loads(request.body)
        new_answer = {}
        for field in Answer._meta.get_all_field_names():
            if field in ['id', 'created', 'question', 'question_id']:
                continue
            if field not in data:
                return HttpResponseBadRequest("Request missing '%s' field" % field)
            if not isinstance(data[field], basestring):
                return HttpResponseBadRequest("Values need to be string type")
            new_answer[field] = data[field]

        Answer.objects.create(question=question, **new_answer)
        return HttpResponse(status=200)

    return HttpResponse(status=404)
