# _*_ encoding:utf-8  _*_


from django.conf.urls import url,include

from .models import Course,Video
from .views import ViesoPlayView

urlpatterns = [
        #视频访问
       #  url(r'^video/(?P<video_id>\d+)/$', ViesoPlayView.as_view(), name="course_video"),
        url(r'^video/(?P<video_id>\d+)/$', ViesoPlayView.as_view(), name="course_video"),
       # url(r'^video/$', ViesoPlayView.as_view(), name="org_list"),
        ]