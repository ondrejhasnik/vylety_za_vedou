#!/usr/bin/env python3
"""
forms.py — Form definitions for the 'vylety' Django application.

Provides forms for user registration and event application.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Application

class RegistrationForm(UserCreationForm):
    """
    Form for user registration extending Django's built-in UserCreationForm.
    Includes additional fields required by CustomUser.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'dob', 'street', 'city',
                  'number', 'postal_code', 'phone', 'school', 'grade', 'id_number']

class ApplicationForm(forms.ModelForm):
    """
    Simple form for applying to an event. Includes an optional note.
    """
    class Meta:
        model = Application
        fields = ['note']
