# _*_ encoding:utf-8  _*_
from django import forms
#验证码用
from captcha.fields import CaptchaField
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)
#必须要和前台登录时的username,pas...一样，之后在views中调用做验证


#验证码
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages= {"invalid":u"验证码错误"})


#找回密码
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages= {"invalid":u"验证码错误"})


#重置密码提交
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)



class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

import re
class UserInfoForm(forms.ModelForm):



    class Meta:
        model = UserProfile
        fields = ['nick_name','gender','birday','address','mobile']

        # 字段验证