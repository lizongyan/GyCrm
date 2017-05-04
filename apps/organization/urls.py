# _*_ encoding:utf-8  _*_


from django.conf.urls import url,include

from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFavView

urlpatterns = [
    # 课程机构首页
     url(r'^list/$', OrgView.as_view(), name="org_list"),
     url(r'^add_ask/$',AddUserAskView.as_view(),name="add_ask"),

     #机构首页
     url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
     #机构课程列表页
     url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
     #机构详情页
     url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
     #教师列表
     url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),
     #收藏
     url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),
]