from django.http import HttpResponse
from core.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import render
from core.models import Profile
from django.contrib.auth.decorators import login_required

@login_required
def leaderboard(request):
    users=Profile.objects.order_by('score')
    users=[i.__dict__ for  i in list(users)]
    user = Profile.objects.get(pk = request.user.pk)
    temp=[{"username":User.objects.get(id=i["user_id"]).__dict__["username"],"score":i["score"]} for i in users]
    final=[]
    temp = temp[::-1]
    temp[0]["index"]=1
    for i in range(len(temp)):
        final.append(temp[i])
        if i>0:
            if final[i]["score"]==final[i-1]["score"]:
                final[i]["index"]=final[i-1]["index"]
            else:
                final[i]["index"]=final[i-1]["index"]+1

    return render(request, 'leaderboard.html', {
        'users': final,
        'score': user.score,
    })

