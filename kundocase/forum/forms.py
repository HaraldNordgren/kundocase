from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Question, Answer


def clean_user_email(self):
    if 'user_name' not in self.cleaned_data:
        return self.cleaned_data['user_email']

    email_lowercase = self.cleaned_data['user_email'].lower()
    if self.cleaned_data['user_name'].lower() == email_lowercase:
        raise ValidationError("User name and email must be different")

    return email_lowercase


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
