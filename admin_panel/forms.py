from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

class AdminProfileForm(UserChangeForm):
      class Meta:
            model = User
            fields = ['username', 'first_name', 'last_name', 'email']


class AdminPasswordChangeForm(PasswordChangeForm):
      class Meta:
            model = User