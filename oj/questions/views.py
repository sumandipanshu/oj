from django.http import HttpResponse
from django.shortcuts import render
from .forms import QuestionForm,SubmissionForm
from .models import Questions,Submission
from .redis_task_add import add_task,get_output
from django.contrib.auth.decorators import login_required

from core.models import Profile
import logging

def get_submission(request):
    solved = Submission.objects.filter(status = "success",user_id = request.user.id)
    submissions = []
    for i in solved:
        temp = {}
        temp["solution"] = i
        temp["question"] = Questions.objects.get(id = i.id)
        submissions.append(temp)
    print(submissions)
    return render(request, 'get_submission.html',{'submissions':submissions})
    

@login_required
def Add_question(request):
    if request.method == 'GET':
        form = QuestionForm()
    else:
        # A POST request: Handle Form Upload
        form = QuestionForm(request.POST) # Bind data from request.POST into a PostForm
 
        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            form.save()
             
    return render(request, 'add_question.html', {
        'form': form,
    })
@login_required
def index(request):
    questions=Questions.objects.all()
    questions=[i.__dict__ for  i in list(questions)]
    user = Profile.objects.get(pk = request.user.pk)
    temp=[]
    for i in questions:
        temp.append({"title":i["title"],"points":i["points"],"id":i["id"]})
    
    logging.warning(temp)
    return render(request,'questions_display.html',{'questions':temp,'score':user.score})

@login_required
def question(request,qid):
    question=Questions.objects.filter(id=qid)[0].__dict__
    logging.warning(question)
    question.pop("test_inputs")
    question.pop("expected_outputs")
    return render(request,"question.html",{"question":question,})

@login_required
def solution(request, qid):
    logging.warning(request.method)
    if request.method=='GET':
        form=SubmissionForm()
        
    else:
        logging.warning(request.user.id)
        logging.warning("ueshissf:r")
        form=SubmissionForm(request.POST)
        submit=Submission()
        previous = Submission.objects.filter(status = "success",user_id = request.user.id, qid = qid)
        logging.warning(previous)
        logging.warning(len(previous))
        if len(previous) == 0:
            if form.is_valid():
                submit=form.save(commit=False)
                submit.qid=qid
                submit.user_id=request.user.id
                submit.status="processing"
                submit.score=0
                submit.save()
            question=Questions.objects.get(id=qid)
            question=question.__dict__
            add_task(request.user.id,qid,submit.solution_code,question["test_inputs"],question["expected_outputs"],submit.lang,submit.status)
            logging.warning(request.user.__dict__)
            user = Profile.objects.get(pk = request.user.pk)
            if user.score == None:
                user.score = 0
            logging.warning(user.__dict__)
            while True:
                if get_output(request.user.id)[b'status'].decode('utf-8')!="processing" and get_output(request.user.id)[b'question'].decode('utf-8')==str(qid):
                    submit = Submission.objects.get(user_id = request.user.id , qid = qid)
                    if get_output(request.user.id)[b"status"].decode('utf-8')=="201":
                        user.score+=int(question["points"])
                        submit.status = "success"
                        submit.save()
                        user.save()
                        logging.warning("\n\n yes \n\n")
                    else:
                        submit.status = "wrong"
                        submit.save()
                    break
    return render(request, 'post_form_upload.html', {
        'form': form,
    })

