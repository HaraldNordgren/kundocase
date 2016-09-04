import json

from django.test import TestCase, RequestFactory

from kundocase.forum.models import Question#, Answer
from kundocase.api.v1 import views


class QuestionTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        Question.objects.create(title="Question1", content="Some content", user_name="Harald",
                                user_email="haraldnordgren@gmail.com")
        Question.objects.create(title="Question2", content="Some more content",
                                user_name="Ronaldo", user_email="ronaldo@cfrm.com")

    def test_get_all_questions(self):
        request = self.factory.get('/api/v1/questions/')
        response = views.questions(request)
        self.assertEqual(response.status_code, 200)

    def test_get_one_question(self):

        request = self.factory.get('/api/v1/questions/1/')
        response = views.questions(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing_question(self):
        request = self.factory.get('/api/v1/questions/4000/')
        response = views.questions(request, 4000)
        self.assertEqual(response.status_code, 404)

    def test_create_with_question_number(self):
        request = self.factory.put('/api/v1/questions/1/')
        response = views.questions(request, 1)
        self.assertEqual(response.status_code, 404)

    def test_incorrect_json(self):
        request = self.factory.put('/api/v1/questions/')
        request.data = {'sdfsd'}
        response = views.questions(request)
        self.assertEqual(response.status_code, 400)

    def test_missing_field(self):
        data = json.dumps({
            "title": "Why is water wet?",
            "user_name": "Harald",
            "user_email": "hej@example.com",
        })
        request = self.factory.put('/api/v1/questions/', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 400)

    def test_non_string_data(self):
        data = json.dumps({
            "title": "Why is water wet?",
            "content": ["Eerer erwerwe ewrewre"],
            "user_name": "Harald",
            "user_email": "hej@example.com",
        })
        request = self.factory.put('/api/v1/questions/', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 400)

    def test_submit_successfully(self):
        data = json.dumps({
            "title": "Why is water wet?",
            "content": "Eerer erwerwe ewrewre",
            "user_name": "Harald",
            "user_email": "hej@example.com",
        })
        request = self.factory.put('/api/v1/questions/', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 200)

    def test_unsupported_request_type(self):
        request = self.factory.delete('/api/v1/questions/')
        response = views.questions(request)
        self.assertEqual(response.status_code, 404)