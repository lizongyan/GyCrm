# _*_ encoding:utf-8  _*_
from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect
#给密码明文加密
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse

from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm
from .models import UserProfile,EmailVerifyRecord
from utils.email_send import send_register_email
# Create your views here.

#自定义登录/在setting中有配置"Custom..."用户名或用邮箱登录
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email = username))
            if user.check_password(password):
                return user
        except Exception as e:
            return  None


#激活邮箱
class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        #如果存在
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            #则返回链接失效
            return render(request, "active_fail.html")
        return  render(request, "login.html")


# 用户注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()  # 验证码
        return render(request, "register.html", {'register_form': register_form})  # 在注册页面调用

    def post(self, request):  # 提交时验证
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            #如果被注册了
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"msg": "用户已经存在","register_form":register_form})

            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user=user_profile.id
            user_message.message= "欢迎注册CRM"
            user_message.save()

            #发送email
            send_register_email(user_name,"register")
            return render(request, "login.html")
        else:
            return render(request, "register.html",{"register_form":register_form})
            #register_form":register_form 用户的回填信息

#退出登录
class LogoutView(View):
    def get(self,request):
        logout(request)

        #传入的index是首页的名称
        return HttpResponseRedirect(reverse("index"))

#基于类完成登录
class LoginView(View):
    def get(self,request):
        return render(request, "login.html",{})
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                 login(request, user)
                 return HttpResponseRedirect(reverse("index"))
                else:
                 return render(request, "login.html",{"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form":login_form})
        #验证字段是否合理



"""
#普通登录验证,上方是基于django类完成登录
def user_login(request):
    if request.method == "POST":
        # 获得前台传过来的
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return render(request, "index.html")
        else:
            return render(request, "login.html",{"msg":"用户名或密码错误！"})
    elif request.method =="GET":#如果没有登录
        return render(request, "login.html", {})
"""
#找回密码
class ForgetPwdView(View):
    def get(self,request):
        return render(request,"forgetpwd.html",{})


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,"forgetpwd.html",{"forget_form":forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email","")
            #发送邮件
            send_register_email(email , 'forget')
            #发送成功则跳转提示页面
            return render(request,"send_success.html")
        else:
            return render(request,"forgetpwd.html",{"forget_form":forget_form})


#找回密码，激活链接
class ResetView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        #如果存在
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html",{"email":email})
        else:
            #则返回链接失效
            return render(request, "active_fail.html")
        return  render(request, "login.html")

#提交重置密码
class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            email = request.POST.get("email","")
            if pwd1 != pwd2:
               return render(request,"password_reset.html",{"email":email,"msg":"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


from utils.mixin_utils import LoginRequiredMixin
from .forms import UserInfoForm
class UserinfoView (LoginRequiredMixin,View):
    """
    用户个人信息
    """
    def get(self,request):
        return render(request,'usercenter-info.html',{})

    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')



class UploadImageView(LoginRequiredMixin,View):
    """
    用户修改头像
    """
    def post(self,request):
        """  一般的修改保存方法
        image_form = UploadImageForm(request.POST,request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image =image
            request.user.save()
            pass
        """
        #使用modelform方法

        image_form = UploadImageForm(request.POST, request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')







import  json
class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

class SendEmailCodeView(LoginRequiredMixin,View):
    """
    发送邮箱验证码
    """
    def get(self,request):
        email = request.GET.get('email','')
        #判断邮箱是否已经注册过了（存在了）
        if UserProfile.objects.filter(email=email):
                return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        #发送邮件
        send_register_email(email,'update_email')

        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    """
    修改个人邮箱
    """
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code', '')
        #是否存在
        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出借"}', content_type='application/json')


class MyCourse(LoginRequiredMixin,View):
    """
    我的课程
    """
    def get(self,request):
        return render(request,'usercenter-mycourse.html',{

        })
#引用收藏表
from operation.models import UserFavorite,UserMessage
from organization.models import CourseOrg
class MyFavOrgView(LoginRequiredMixin,View):
    """
    我收藏的课程机构
    """
    def get(self,request):
        #定义一个空集合
        org_list =[]
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org =CourseOrg.objects.get(id=org_id)
            #填充list
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{
            "org_list":org_list
        })

class MyFavTeacherView(LoginRequiredMixin,View):
    """
    我收藏的课程机构
    """
    def get(self,request):

        return render(request,'usercenter-fav-teacher.html',{
        })


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
class MymessageView(LoginRequiredMixin,View):
    """
    我的消息
    """
    def get(self,request):
       # all_message = UserMessage.objects.all()
       #只取当前登录人的消息，
        all_message = UserMessage.objects.filter(user=request.user.id)
        #用户进入个人消息，消息状态变为已读
        all_unread_message = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 1, request=request)
        message = p.page(page)

        # 总家数
        org_nums = all_message.count()

        return render(request,'usercenter-message.html',{
            "message":message

        })


from .models import Banner
from courses.models import Course
#首页功能
class IndexView(View):
    def get(self,request):
        #取现轮播图
        all_banners = Banner.objects.all().order_by('index')
        #取课程
        course = Course.objects.filter(is_banner=False)[:5]
        banner_course= Course.objects.filter(is_banner=False)[:3]

        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html',{
            'all_banners':all_banners,
            'course':course,
            'banner_course':banner_course,
            'course_orgs':course_orgs
        })

def page_not_found(request):
    #合局404修理函数
    from django.shortcuts import render_to_response
    response=render_to_response('404.html',{})
    response.status_code = 404
    return response
def page_error(request):
    #合局500修理函数
    from django.shortcuts import render_to_response
    response=render_to_response('500.html',{})
    response.status_code = 500
    return response