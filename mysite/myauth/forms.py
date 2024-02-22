from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    '''ModelForm - генерирует форму на основе существующей модели'''
    class Meta:
        model = Profile
        fields = ("avatar",)
