# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Profile

from django import forms 

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['homepage', 'avatar' ]