# _*_ encoding:utf-8  _*_

from django.conf.urls import url,include

from .views import UserinfoView,UploadImageView,UpdatePwdView,SendEmailCodeView,UpdateEmailView,MyCourse
from .views import MyFavOrgView,MyFavTeacherView,MymessageView
urlpatterns = [
        #用户信息
        url(r'^info/$', UserinfoView.as_view(), name="user_info"),

        #用户头像上传
        url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),

        #用户个人中心修改密码
        url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),

        #发送邮箱验证码
        url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
        # 修改邮箱
        url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
        # 我的课程
        url(r'^mycourse/$', MyCourse.as_view(), name="mycourse"),
        # 我的收藏的课程机构
        url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),
        # 我的收藏讲师
        url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
        # 我的消息
        url(r'^mymessage/$', MymessageView.as_view(), name="mymessage"),
]