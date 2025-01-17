from django.db.models import query
from django.shortcuts import redirect, render
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http.response import HttpResponse, JsonResponse, StreamingHttpResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.views.generic import View
from django.contrib.sites.shortcuts import get_current_site
from .models import User_info
from widget.models import Layout
from .tokens import account_activation_token
from .text import message
import hashlib


class Activate(View):
  def get(self, request, uidb64, token):
    try:
      uid = force_text(urlsafe_base64_decode(uidb64))
      user = User_info.objects.get(pk=uid)
      if account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')

      return JsonResponse({"message": "AUTH FAIL"}, status=400)

    except ValidationError:
        return JsonResponse({"message": "TYPE_ERROR"}, status=400)
    except KeyError:
        return JsonResponse({"message": "INVALID_KEY"}, status=400)


def login_view(request):


  # @FIXME: Remove this after login func is implemented
  if 'user_email' in request.session:
    return redirect('home')

  return render(request, 'login.html')


def logout(request):
  del request.session['user_email']
  return redirect('login_view')


def join_view(request):
  return render(request, 'join.html')


def login_action(request):
  email = request.POST.get('email')
  raw_pw = request.POST.get('raw_pw')
  # HashedPasswordObj =hashlib.sha1(raw_pw.encode('UTF-8'))
  # HashedPassword = HashedPasswordObj.hexdigest()
  queryset = User_info.objects.filter(user_email = email, user_pwd = raw_pw)
  
  if len(queryset) == 1 :
    request.session['user_email'] = email
    return redirect('home')
    # if queryset[0]['is_active'] :
    #   # return redirect('main')
    #   pass
    # # is_active == False : email 인증 단계로 
    #   pass

  return render(request, 'login.html',{'message':True})


def join_action(request):
  data = request.POST
  # HashedPasswordObj =hashlib.sha1(data.get('user_pwd', False).encode('UTF-8'))
  # HashedPassword = HashedPasswordObj.hexdigest()
  User_info.objects.create(user_email=data.get('user_email', False), user_pwd=data.get('user_pwd'), user_name=data.get('user_name', False))
  QS = User_info.objects.filter(user_email=data.get('user_email', False), user_pwd=data.get('user_pwd'), user_name=data.get('user_name', False))
  Layout.objects.create(creater=QS[0], owner=QS[0], is_applied=True, data="[]", from_store=False)
  return redirect('login_view')


def join_email_overap(request):
  email = request.GET['email']
  queryset = User_info.objects.filter(user_email = email)
  if len(queryset) > 0:
    return HttpResponse('Overap')
  return HttpResponse('Usable')


def send_validation_mail(request, user, email_address):
    mail_title = "DoMain 이메일 인증을 완료해주세요."
    domain = get_current_site(request).domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    mail_data = message(domain, uidb64, token)
    mail_to = email_address
    email = EmailMessage(mail_title, mail_data, to=[mail_to])
    email.send()


def is_sess_attached(request):
  is_sess = False
  if 'user_email' in request.session:
    is_sess = True
  return is_sess


def get_user_inst(request):
  if is_sess_attached(request):
    email = request.session['user_email']
    queryset = User_info.objects.filter(user_email = email)
    return queryset[0]


def is_login(request):
  if 'user_email' in request.session:
    return HttpResponse('true')
  return HttpResponse('false')