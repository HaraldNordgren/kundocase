from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Question, Answer


def clean_user_email(self):
    if 'user_name' not in self.cleaned_data:
        return self.cleaned_data['user_email']

    if self.cleaned_data['user_name'] == self.cleaned_data['user_email']:
        raise ValidationError("User name and email must be different")

    return self.cleaned_data['user_email']


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'user_name', 'user_email']

    clean_user_email = clean_user_email

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'user_name', 'user_email']

    clean_user_email = clean_user_email
