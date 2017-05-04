# _*_ encoding:utf-8  _*_
import xadmin
from xadmin import views
from .models import Lesson,Course,CourseResource,Video

class CourseAdmin(object):
    pass

class LessonAdmin(object):
    pass

class CourseResourceAdmin(object):
    pass

class VideoResourceAdmin(object):
    pass

xadmin.site.register(Video,VideoResourceAdmin)
xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)