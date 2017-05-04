# _*_ encoding:utf-8  _*_
from django.shortcuts import render

from django.views.generic import View
# Create your views here.
from .models import Course,Video

class ViesoPlayView(View):
    """
    视频播放页面
    """
    def get(self,request,video_id):


       video = Video.objects.get(id=int(video_id))
       course = video.lesson.course
       course.studen +=1
        #播放加1
       course.save()

       return render(request, 'course-play.html', {
           "video":video
       }
       #前段查看（http://127.0.0.1:8000/course/video/1/）  1是传的ID

                     )