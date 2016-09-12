import json

from django.core import serializers
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest


def get_json(asset_id, model, objects):
    if asset_id:
        try:
            question_or_answer = objects.get(id=asset_id)
        except model.DoesNotExist:
            return HttpResponse(status=404)

        raw_data = serializers.serialize('python', [question_or_answer])[0]
        return_data = raw_data['fields']
        return_data['id'] = raw_data['pk']
        return JsonResponse(return_data)
    else:
        raw_data = serializers.serialize('python', objects.all().order_by("created"))
        return_data = []
        for asset in raw_data:
            element = asset['fields']
            element['id'] = asset['pk']
            return_data.append(element)
        return JsonResponse(return_data, safe=False)


def put_json(asset_id, body, model, objects, excluded_fields, parent_question=None):
    if not body:
        return HttpResponseBadRequest("Request body is empty")

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
        new_data['question'] = parent_question

    if asset_id:
        row = objects.filter(id=asset_id)
        if not row:
            return HttpResponse(status=404)
        row.update(**new_data)
        return HttpResponse(status=200)
    else:
        model.objects.create(**new_data)
        return HttpResponse(status=201)
