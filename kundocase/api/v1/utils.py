import json

from django.core import serializers
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest


def get_json(question_or_answer_id, model, objects):
    if question_or_answer_id:
        try:
            question_or_answer = objects.get(id=question_or_answer_id)
        except model.DoesNotExist:
            return HttpResponse(status=404)

        raw_data = serializers.serialize('python', [question_or_answer])[0]
        return JsonResponse(raw_data['fields'])
    else:
        raw_data = serializers.serialize('python', objects.all().order_by("created"))
        actual_data = [question['fields'] for question in raw_data]
        return JsonResponse(actual_data, safe=False)


def put_json(question_or_answer_id, body, model, excluded_fields, parent_question=None):
    if question_or_answer_id:
        return HttpResponse(status=404)

    try:
        data = json.loads(body)
    except ValueError:
        return HttpResponseBadRequest("Request body is incorrect JSON")

    new_data = {}
    for field in model._meta.get_all_field_names():
        if field in excluded_fields:
            continue
        if field not in data:
            return HttpResponseBadRequest("Request is missing '%s' field" % field)
        if not isinstance(data[field], basestring):
            return HttpResponseBadRequest("Values need to be string type")
        new_data[field] = data[field]

    if parent_question:
        model.objects.create(question=parent_question, **new_data)
    else:
        model.objects.create(**new_data)

    return HttpResponse(status=200)
