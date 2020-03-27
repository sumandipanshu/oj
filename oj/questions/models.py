from django.db import models

class Questions(models.Model):
    title=models.CharField(max_length=80,blank=False)
    description=models.TextField(max_length=300,blank=False)
    points=models.IntegerField(null=False,blank=False)
    test_inputs=models.TextField(max_length=300,blank=False)
    expected_outputs=models.TextField(max_length=300,blank=False)
    author=models.CharField(max_length=30,blank=True)
class Submission(models.Model):
    qid=models.IntegerField(null=False,blank=False)
    user_id=models.IntegerField(null=False,blank=False)
    solution_code=models.TextField(null=False,blank=False)
    lang=models.CharField(max_length=80,null=False,blank=False)
    status=models.CharField(max_length=10,null=False,blank=False)
    score=models.IntegerField(null=False,blank=False)