from django import forms
from django.forms import fields
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name', 'url', 'notes']