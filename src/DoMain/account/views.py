from django.shortcuts import redirect, render
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http.response import HttpResponse, JsonResponse, StreamingHttpResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.views.generic import View
from django.contrib.sites.shortcuts import get_current_site
from .models import User_info
from .tokens import account_activation_token
from .text import message

from .forms import UserForm
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
  return render(request, 'login.html')


def join_view(request):
  return render(request, 'join.html')


def login_action(request):
  pass


def join_action(request):
  data = request.POST
  HashedPasswordObj =hashlib.sha1(data.get('user_pwd', False).encode('UTF-8'))
  HashedPassword = HashedPasswordObj.hexdigest()
  User_info.objects.create(user_email=data.get('user_email', False), user_pwd=HashedPassword, user_name=data.get('user_name', False))
  return redirect('login_view')


def send_validation_mail(request, user, email_address):
    mail_title = "DoMain 이메일 인증을 완료해주세요."
    domain = get_current_site(request).domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    mail_data = message(domain, uidb64, token)
    mail_to = email_address
    email = EmailMessage(mail_title, mail_data, to=[mail_to])
    email.send()

