import json

from django.shortcuts import get_object_or_404
from django.core import serializers
from django.http import JsonResponse
from kundocase.forum.models import Question


def questions(request, question_id=None):

    if request.method == 'GET':
        if question_id:
            question = get_object_or_404(Question, id=question_id)
            raw_data = serializers.serialize('python', [question])[0]
            return JsonResponse(raw_data['fields'])
        else:
            raw_data = serializers.serialize('python', Question.objects.all().order_by("created"))
            actual_data = [question['fields'] for question in raw_data]
            return JsonResponse(actual_data, safe=False)
