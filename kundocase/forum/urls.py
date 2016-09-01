from django.conf.urls import url
from kundocase.forum.views import startpage, question, add_question

urlpatterns = [
    url(r"^$", startpage, name="startpage"),
    url(r"^(?P<id>\d+)$", question, name="question"),
    url(r"^add_question$", add_question, name="add_question")
]
