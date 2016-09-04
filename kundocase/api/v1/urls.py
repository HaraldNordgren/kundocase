from django.conf.urls import url

from .views import questions


urlpatterns = [
    url(r"^questions/$", questions),
    url(r"^questions/(?P<question_id>\d+)/$", questions),
]
