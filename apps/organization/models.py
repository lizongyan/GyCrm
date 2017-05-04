# _*_ encoding:utf-8  _*_
from __future__ import unicode_literals
from datetime import datetime
from django.contrib.staticfiles.templatetags import staticfiles
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from gycrm.settings import MEDIA_URL


class CityDict(models.Model):
    #不可重复，重复则提醒
    name = models.CharField(max_length=20, verbose_name = u'城市',unique=True,
                            error_messages={
                                'unique': _("A user with that username already exists."),
                            }
                            )
    desc = models.CharField(max_length=200, verbose_name = u"描述")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

#课程机构
class CourseOrg(models.Model):
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"logo", max_length=200)
    name = models.CharField(max_length=50,verbose_name=u"机构名称")
    desc = models.TextField(verbose_name=u"机构描述")
    tag = models.CharField(max_length=10,verbose_name=u"机构标签",default="全国知名")
    category = models.CharField(verbose_name=u"机构类别",max_length=20,choices=(("pxjg","培训机构"),("gr","个人"),("gx","高校")),default="pxjg")
    click_nums = models.IntegerField(default=0,verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0,verbose_name=u"收藏数")
    address = models.CharField(max_length=150, verbose_name=u"机构地址")
    city = models.ForeignKey(CityDict,verbose_name=u"所在城市")
    students = models.IntegerField(default=0,verbose_name=u"学习人数")
    course_nums = models.IntegerField(default=0,verbose_name=u"课程数")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程机构"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_img(self):
        from django.utils.safestring import mark_safe
        ass=str(self.image)
        return mark_safe("<img width='100px' height='100px' class='scrollLoading' src='"+MEDIA_URL+""+ass+"'/>")
    get_img.short_description = "学员头像"
#{{ MEDIA_URL }}{{ cours_org.image }}


#教师表
class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,verbose_name=u"所属机构")
    name = models.CharField(max_length=50,verbose_name=u"老师名")
    work_years = models.IntegerField(default=0,verbose_name=u"工作年限")
    work_company = models.CharField(max_length=50,verbose_name=u"就职公司",default="")
    work_position = models.CharField(max_length=50,verbose_name=u"公司职位",default="")
    points = models.CharField(max_length=50,verbose_name=u"教学特点",default="")
    click_nums = models.IntegerField(default=0,verbose_name=u"点击数")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", default='', max_length=100)

    fav_nums = models.IntegerField(default=0,verbose_name=u"收藏数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"老师"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name