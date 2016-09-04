from django.conf.urls import url

from .views import questions, answers


urlpatterns = [
    url(r"^questions/(?P<question_id>\d+)/answers/$", answers),
    url(r"^questions/(?P<question_id>\d+)/answers/(?P<answer_id>\d+)/$", answers),

    url(r"^questions/$", questions),
    url(r"^questions/(?P<question_id>\d+)/$", questions),
]
