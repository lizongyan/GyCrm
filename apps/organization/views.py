# _*_ encoding:utf-8  _*_
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg,CityDict
from courses.models import Course

class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self,request):
        #课程机构
        all_orgs = CourseOrg.objects.all()

        #取出热门的（根据字段click_nums排序取出前三个）
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        #城市
        all_city = CityDict.objects.all()

        #机构全局搜索
        search_keywords = request.GET.get('keywords',"")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))




        #取出筛选城市
        city_id = request.GET.get('city',"")

        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #类别筛选
        category = request.GET.get('ct', "")

        if category:
            all_orgs = all_orgs.filter(category=category)
        #排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'students':

                all_orgs = all_orgs.order_by("-students")
            elif sort == "course":
                all_orgs = all_orgs.order_by("-course_nums")
        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 1,request=request)
        orgs = p.page(page)

        #总家数
        org_nums = all_orgs.count()
        return render(request,"org-list.html",{
            "all_orgs":orgs,
            "all_city":all_city,
            "org_nums":org_nums,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort,
        })

from .forms import UserAskForm
#ajax返回数据
from django.http import HttpResponse
class AddUserAskView(View):
    """
    用户添加资讯
    """

    def post(self,request):
        #验证字段是否合理
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            #直接提交保存
            user_ask = userask_form.save(commit=True)
            #成功则返回如下,返回异步提交成功的提示 ，后面的content_type是固定的写法,不要变
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            #失败则返回如下，
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self,request,org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id = int(org_id))
        # 是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        #取出了所有课程，（课程是外键
        all_courses = course_org.course_set.all()[:3]

        return  render(request,'org-detail-homepage.html',
                       {
                           'all_course':all_courses,
                            'course_org':course_org,
                           'current_page':current_page,
                           'has_fav':has_fav
                       }
                    )


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self,request,org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id = int(org_id))
        # 是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True


        #取出了所有课程，（课程是外键
        all_courses = course_org.course_set.all()
        all_teachers = course_org.teacher_set.all()
        return  render(request,'org-detail-course.html',
                       {
                           'all_course':all_courses,
                           'all_teachers':all_teachers,
                            'course_org':course_org,
                           'current_page':current_page,
                           'has_fav':has_fav
                       }
                    )


class OrgDescView(View):
    """
    机构介绍页
    """
    def get(self,request,org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id = int(org_id))
        # 是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        #取出了所有课程，（课程是外键
        return  render(request,'org-detail-desc.html',
                       {
                            'course_org':course_org,
                           'current_page':current_page,
                           'has_fav':has_fav
                       }
                    )


class OrgTeacherView(View):
    """
    机构老师页
    """
    def get(self,request,org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id = int(org_id))
        # 是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        #取出了所有课程，（课程是外键
        all_teachers = course_org.teacher_set.all()
        return  render(request,'org-detail-teachers.html',
                       {
                           'all_teachers':all_teachers,
                            'course_org':course_org,
                           'current_page':current_page,
                           'has_fav':has_fav
                       }
                    )


from operation.models import UserFavorite
class AddFavView(View):
    """
    用户收藏功能,用户取消收藏
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)
        #用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        #用户是否存在
        exist_recodes = UserFavorite.objects.filter(user = request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_recodes:
            #如果存在则取消收藏,删除
            exist_recodes.delete()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0 :
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')

            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')

























