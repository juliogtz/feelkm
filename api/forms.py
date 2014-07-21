from django import forms
from django.forms import ModelForm

class UploadPics(forms.Form):
    file1 = forms.ImageField()
    file2 = forms.ImageField()
    file3 = forms.ImageField()
    id_event_ = forms.HiddenInput()
    urlevent = forms.HiddenInput()


