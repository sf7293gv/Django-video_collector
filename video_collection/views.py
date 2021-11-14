from django.shortcuts import render

def home(request):
    return render(request, 'video_collection/home.html')