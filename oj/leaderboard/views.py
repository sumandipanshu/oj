from django.http import HttpResponse
from core.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import render

def leaderboard(request):
    users=Profile.objects.order_by('score')
    users=[i.__dict__ for  i in list(users)]
    temp=[{"username":User.objects.get(id=i["user_id"]).__dict__["username"],"score":i["score"]} for i in users]
    print(temp)
    return render(request, 'leaderboard.html', {
        'users': temp[::-1],
    })

