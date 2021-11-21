from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add', views.add, name='add_video'),
    path('video_list', views.video_list, name='video_list'),
    path('about_video/<int:video_pk>', views.about_video, name='about_video'),
    path('delete_video/<int:video_pk>', views.delete_video, name='delete_video')
]