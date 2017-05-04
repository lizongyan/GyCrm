# _*_ encoding:utf-8  _*_
"""gycrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from organization.views import OrgView
from django.views.static import serve
import xadmin

from gycrm.settings import MEDIA_ROOT,STATIC_ROOT
from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView,LogoutView
from users.views import IndexView
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    #url('^$', TemplateView.as_view(template_name="index.html"),name="index"),
    url('^$', IndexView.as_view(), name="index"),
    #前台点击登录按钮时跳转
    url('^login/', LoginView.as_view(), name="login"),
    #退出登录
    url('^logout/', LogoutView.as_view(), name="logout"),
    #注册
    url('^register/', RegisterView.as_view(), name="register"),
    #注册码
    url(r'^captcha/', include('captcha.urls')),
    #激活邮箱验证码链接
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name="user_active" ),
   # url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),
    #找回密码
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    #重置密码访问
    url(r'^reset/(?P<active_code>.*)/$',ResetView.as_view(),name="reset_pwd" ),
    #提交重置密码
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    #课程机构首页
   # url(r'^org_list/$', OrgView.as_view(), name="org_list"),

    #配置课程机构url、、、、namespace命名空间
    url(r'^org/', include('organization.urls',namespace="org")),
    #配置课程的urls
    url(r'^course/', include('courses.urls',namespace="course")),
    #配置user的urls
    url(r'^users/', include('users.urls', namespace="users")),

    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT})
]

#全局500 404
handler404 = 'users.views.page_not_found'
handler500='users.views.page_error'