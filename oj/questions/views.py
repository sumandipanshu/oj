from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import QuestionForm,SubmissionForm
from .models import Questions,Submission
from .redis_task_add import add_task,get_output
from django.contrib.auth.decorators import login_required
import threading
from core.models import Profile
import logging

@login_required
def get_submission(request):
    # symbols = '< > & \' \"'.split()
    # replace = '&lt; &gt; &amp; &apos; &quot;'.split()
    solved = Submission.objects.filter(user_id = request.user.id)
    submissions = []
    for i in solved:
        temp = {}
        temp["solution"] = i
        # for sym,rep in zip(symbols,replace):
        #     temp["solution"].solution_code = temp["solution"].solution_code.replace(sym,rep)
        temp["question"] = Questions.objects.get(id = i.qid)
        submissions.append(temp)
    return render(request, 'get_submission.html',{'submissions':submissions[::-1]})
    

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
    
    return render(request,'questions_display.html',{'questions':temp,'score':user.score})

@login_required
def question(request,qid):
    question=Questions.objects.filter(id=qid)[0].__dict__
    question.pop("test_inputs")
    question.pop("expected_outputs")
    return render(request,"question.html",{"question":question,})

@login_required
def solution(request, qid):
    logging.warning(request.method)
    if request.method=='GET':
        form=SubmissionForm()
        return render(request, 'post_form_upload.html', {'form': form})
        
    else:
        form=SubmissionForm(request.POST)
        submit=Submission()
        previous = Submission.objects.filter(status = "success",user_id = request.user.id, qid = qid)
        flag = 0
        if len(previous) == 0:
            flag=1
        else:
            flag=0

        if form.is_valid():
            submit=form.save(commit=False)
            submit.qid=qid
            submit.user_id=request.user.id
            submit.status="processing"
            submit.score=0
            submit.save()
            th = threading.Thread(target = handle_submission, args = (request.user.id,qid,submit,flag,))
            th.start()

        
        return redirect(get_submission)

def handle_submission(user_id,qid,submit,flag):
    question=Questions.objects.get(id=qid)
    add_task(user_id,qid,submit.solution_code,question.test_inputs,question.expected_outputs,submit.lang,submit.status,question.time_limit)
    user = Profile.objects.get(pk = user_id)
    if user.score == None:
        user.score = 0
    while True:
        compiler_output = get_output(user_id)
        if compiler_output[b'status'].decode('utf-8')!="processing" and compiler_output[b'question'].decode('utf-8')==str(qid):
            if compiler_output[b"status"].decode('utf-8')=="201":
                if flag == 1:
                    user.score+=int(question.points)
                    user.save()
            submit.status = compiler_output[b"status"].decode('utf-8')
            submit.save()
            break
    
