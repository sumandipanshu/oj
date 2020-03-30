from django.forms import ModelForm
from .models import Questions,Submission

class QuestionForm(ModelForm):
    class Meta:
        model=Questions
        fields='__all__'

class SubmissionForm(ModelForm):
    class Meta:
        model=Submission
        fields=('lang','solution_code',)
