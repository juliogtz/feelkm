from django import forms
from django.forms import ModelForm

class UploadPics(forms.Form):
    file1 = forms.ImageField(upload_to='/media')
    file2 = forms.ImageField(upload_to='/media')
    file3 = forms.ImageField(upload_to='/media')
    id_event_ = forms.HiddenInput()
    urlevent = forms.HiddenInput()


