# _*_ encoding:utf-8  _*_
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from organization.models import CourseOrg

# Create your models here.

"""
课程
"""
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name=u"课程机构",null=True,blank=True)
    name = models.CharField(max_length=50,verbose_name=u"课程名")
    desc = models.CharField(max_length=300,verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(choices=(("初级", "初级"), ("中级", "中级"), ("高级", "高级")), max_length=2, default="cj")
    email = models.EmailField(max_length=20, verbose_name=u"邮箱", default="")
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    studen = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏")
    image = models.ImageField(upload_to="image/%Y/%m", verbose_name="封面图", default=u"image/default.png", max_length=100)
    #是否为广告位
    is_banner = models.BooleanField(default=False,verbose_name=u"是否轮播")
    click_number = models.IntegerField(default=0, verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = "课程复件"
        verbose_name_plural = verbose_name
        proxy = True

"""
章节
"""
class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100,verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添中时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0}".format(self.name)


"""
视频
"""
class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u"章节")
    name = models.CharField(max_length=120,verbose_name=u"视频名")
    url = models.CharField(max_length=120,verbose_name=u"路径",default="")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"详细章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0}".format(self.name)


"""
课程资源
"""
class CourseResource(models.Model):
    coerce = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=120,verbose_name=u"视频名")
    download = models.FileField(upload_to="course/resource/%Y/m",verbose_name=u"资源文件",max_length=100)
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name