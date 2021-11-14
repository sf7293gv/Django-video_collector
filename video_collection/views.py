from django.shortcuts import render

def home(request):
    app_name = 'MMA Videos Collector'
    return render(request, 'video_collection/home.html', {'app_name': app_name})