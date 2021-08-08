from django.http import request, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from store.models import StoreWidget
from store.models import Comment, Reply
from account.models import User_info
import json
from django.utils import timezone
from datetime import datetime


def landing_page(request):
    return render(request, 'landingPage.html')

def store_main(request):
    return render(request, 'AssetStoreMainPage.html')

def subpage(request):
    widgets = StoreWidget.objects.all()
    return render(request, 'subpage.html', {'widgets':widgets})

def detailpage(request, id):
    widget = get_object_or_404(StoreWidget, seq=id)
    # comment = get_object_or_404(Comment, id=id)
    comments = Comment.objects.filter(widget=widget)
    
    return render(request, 'detailpage.html', {"widget":widget, "comments":comments, "replys":replys})

def mypage(request):
    return render(request, 'myPage.html')

def comment_write(request):
    email= request.session['user_email']
    user = User_info.objects.get(user_email=email)

    if request.method == "GET":
        comment = Comment()
        comment.writer = user
        comment.widget = get_object_or_404(StoreWidget, seq=request.POST.get('widget_id'))
        comment.content = request.POST.get('body')
        comment.save()

        dt_now = datetime.now()
        ampm = dt_now.strftime('%p')
        ampm_kr = '오전' if ampm == 'AM' else '오후'
    
        ret = {
            'body': comment.content,
            'time': dt_now.strftime(f"%Y년 %#m월 %#d일 %I:%M {ampm_kr}"
            .encode('unicode-escape').decode())
            .encode().decode('unicode-escape'),
            'user': comment.writer.user_name
        }
        return HttpResponse(json.dumps(ret), content_type="application/json")
        

def reply_comment(request):
    email= request.session['user_email']
    user = User_info.objects.get(user_email=email)
    

    if request.method == "GET":
    
        ret = {
            # body를 가져올 필요가 없다?고 하셨던 것 같은데 그러면 내용은 우예 가져오나요
            'body':reply.content,
            'time': dt_now.strftime(f"%Y년 %#m월 %#d일 %I:%M {ampm_kr}"
            .encode('unicode-escape').decode())
            .encode().decode('unicode-escape'),
            'user': reply.writer.user_name
        }
        return HttpResponse(json.dumps(ret), content_type="application/json")