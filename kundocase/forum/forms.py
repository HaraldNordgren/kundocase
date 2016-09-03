from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Question

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'user_name', 'user_email']

    def clean_user_email(self):
        if self.cleaned_data['user_name'] == self.cleaned_data['user_email']:
            raise ValidationError("User name and email must be different")

        return self.cleaned_data['user_email']