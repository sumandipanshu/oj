from django.forms import ModelForm
from .models import Questions,Submission

class QuestionForm(ModelForm):
    class Meta:
        model=Questions
        fields=('title','description','points','test_inputs','expected_outputs','author',)

class SubmissionForm(ModelForm):
    class Meta:
        model=Submission
        fields=('lang','solution_code',)