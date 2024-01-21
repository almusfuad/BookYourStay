from django import forms
from . models import Transaction

class DepositForm(forms.ModelForm):
      class Meta:
            model = Transaction
            fields = ['amount']