# _*_ encoding:utf-8  _*_
from xadmin.plugins.auth import UserAdmin
import xadmin
from xadmin import views
from django.db.models import Q
from .models import CityDict,CourseOrg,Teacher


class CityDictAdmin(object):
    list_filter = ['name']
    menu_index = 1
    order = 2
class CourseOrgAdmin(object):
    show_detail_fields = ('name',)
    list_display = ["get_img",'name','desc','category',]
    show_detail_fields = ('id','get_img',)
    list_editable = [ "name"]


    #数据过滤用
    def queryset(self):
        qs = super(CourseOrgAdmin,self).queryset()
        qs = qs.filter(Q(city = 1) | Q(city = 2))
        return qs
class TeacherAdmin(object):
    pass







xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(CityDict, CityDictAdmin)