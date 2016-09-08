import json

from django.test import TestCase, RequestFactory

from kundocase.forum.models import Question, Answer
from kundocase.api.v1 import views


class QuestionTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        Question.objects.create(title="Question 1",
                                content="Some content",
                                user_name="Harald",
                                user_email="haraldnordgren@gmail.com")
        Question.objects.create(title="Question 2",
                                content="Some more content",
                                user_name="Ronaldo",
                                user_email="ronaldo@realmadrid.com")

    def test_get_all_questions(self):
        request = self.factory.get('/api/v1/questions/')
        response = views.questions(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_get_one_question(self, content_value="Some content"):
        request = self.factory.get('/api/v1/questions/1/')
        response = views.questions(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['content'], content_value)

    def test_get_non_existing_question(self):
        request = self.factory.get('/api/v1/questions/4000/')
        response = views.questions(request, 4000)
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

    def test_submit_question_successfully(self):
        data = json.dumps({
            "title": "Why is water wet?",
            "content": "Eerer erwerwe ewrewre",
            "user_name": "Harald",
            "user_email": "hej@example.com",
        })
        request = self.factory.put('/api/v1/questions/', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 201)

    def test_update_question(self):
        data = json.dumps({
            "title": "Why is water wet?",
            "content": "Some new content",
            "user_name": "Harald",
            "user_email": "hej@example.com",
        })
        request = self.factory.put('/api/v1/questions/1/', data=data)
        response = views.questions(request, 1)
        self.assertEqual(response.status_code, 200)
        self.test_get_one_question("Some new content")

    def test_unsupported_request_type(self):
        request = self.factory.delete('/api/v1/questions/')
        response = views.questions(request)
        self.assertEqual(response.status_code, 405)


class AnswerTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        q1 = Question.objects.create(title="Question1",
                                     content="Some content",
                                     user_name="Harald",
                                     user_email="haraldnordgren@gmail.com")
        q2 = Question.objects.create(title="Question2",
                                     content="Some more content",
                                     user_name="Ronaldo",
                                     user_email="ronaldo@cfrm.com")

        Answer.objects.create(content="Some content",
                              user_name="Harald",
                              user_email="haraldnordgren@gmail.com",
                              question=q1)
        Answer.objects.create(content="Some more content",
                              user_name="Harry",
                              user_email="haraldnordgren@gmail.com",
                              question=q1)

    def test_get_all_answers_for_question(self):
        request = self.factory.get('/api/v1/questions/1/answers/')
        response = views.answers(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_get_one_answer(self, user_value="Harry"):
        request = self.factory.get('/api/v1/questions/1/answers/2/')
        response = views.answers(request, 1, 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['user_name'], user_value)

    def test_get_empty_answers_for_question(self):
        request = self.factory.get('/api/v1/questions/2/answers/')
        response = views.answers(request, 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_get_non_existing_answer(self):
        request = self.factory.get('/api/v1/questions/1/answers/8000/')
        response = views.answers(request, 1, 8000)
        self.assertEqual(response.status_code, 404)

    def test_incorrect_json(self):
        request = self.factory.put('/api/v1/questions/1/answers/')
        request.data = {'sdfsd'}
        response = views.answers(request, 1)
        self.assertEqual(response.status_code, 400)

    def test_missing_field(self):
        data = json.dumps({
            "user_name": "Harald",
            "user_email": "hej@example.com",
        })
        request = self.factory.put('/api/v1/questions/1/answers/', data=data)
        response = views.answers(request, 1)
        self.assertEqual(response.status_code, 400)

    def test_non_string_data(self):
        data = json.dumps({
            "content": ["Lorem ipsum dolor sit amet"],
            "user_name": "Harald",
            "user_email": "hej@example.com",
        })
        request = self.factory.put('/api/v1/questions/1/answers/', data=data)
        response = views.answers(request, 1)
        self.assertEqual(response.status_code, 400)

    def test_submit_answer_successfully(self):
        data = json.dumps({
            "content": "Lorem ipsum dolor sit amet",
            "user_name": "Harald",
            "user_email": "hej@example.com",
        })
        request = self.factory.put('/api/v1/questions/1/answers/', data=data)
        response = views.answers(request, 1)
        self.assertEqual(response.status_code, 201)

    def test_update_answer(self):
        data = json.dumps({
            "content": "Some new content",
            "user_name": "Harald",
            "user_email": "hej@example.com",
        })
        request = self.factory.put('/api/v1/questions/1/answers/2/', data=data)
        response = views.answers(request, 1, 2)
        self.assertEqual(response.status_code, 200)
        self.test_get_one_answer("Harald")

    def test_unsupported_request_type(self):
        request = self.factory.delete('/api/v1/questions/1/answers/')
        response = views.answers(request, 1)
        self.assertEqual(response.status_code, 405)
