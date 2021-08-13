from django.contrib.auth.forms import UserChangeForm
from .models import User_info
import models
import forms
    
class ProfileForm(models.Model):
    image = forms.ImageField(label="이미지", required=False)
   	# 위의 내용을 정의하지 않아도 상관없지만, 화면에 출력될 때 label이 영문으로 출력되는 것이 싫어서 수정한 것이다..
    class Meta:
        model = User_info
        fields = ['image',]