from django.shortcuts import render
from django.contrib import messages
from .forms import VideoForm
from .models import Video

def home(request):
    app_name = 'MMA Videos Collector'
    return render(request, 'video_collection/home.html', {'app_name': app_name})

def add(request):
    if request.method == 'POST':
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid():
            new_video_form.save()
            messages.info(request, 'New Video Saved')
            #todo show success message or redirect
        else:
            messages.warning(request, 'Enter valid data')
            return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})


def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_collection/video_list.html', {'videos': videos})