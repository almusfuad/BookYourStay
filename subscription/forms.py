from django import forms
from .models import Subscriber


class SubscriberForm(forms.ModelForm):
      class Meta:
            fields = Subscriber
            fields = ['email']