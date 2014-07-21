from django import forms
from django.forms import ModelForm
from api.models import photos

class UploadPics(ModelForm):
    class Meta:
       model = photos
       fields = ['file1','file2','file3']


