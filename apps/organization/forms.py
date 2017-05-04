# _*_ encoding:utf-8  _*_

from django import forms
from operation.models import UserAsk

#传统Form
#class UserAskForm(forms.Form):
   # name = forms.CharField(required=True,min_length=2,max_length=20)
   # phone = forms.CharField(required=True,min_length=11,max_length=11)
  #  course_name = forms.CharField(required=True,min_length=5,max_length=50)
import re
#modelform
class UserAskForm(forms.ModelForm):
   # my_filed = forms.CharField()  可以新增字段...
    class Meta:
        model = UserAsk
        #要验证的字段
        fields = ['name','mobile','course_name']
     #字段验证
    def clean_mobile(self):
        """
        验证手机号码
        """
        mobile = self.cleaned_data['mobile']
        #手机正则表达式验证
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")



