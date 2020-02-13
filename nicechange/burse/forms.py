from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from burse.models import Profile
from django import forms
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',  'email')
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'two', 'history', 'trade_rules')

class StatForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('dealscount', 'uniquedealscount')