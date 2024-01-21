from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student

class RegistrationForm(UserCreationForm):
      email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
      phone = forms.CharField(max_length=15)
      country = forms.CharField(max_length=50)
      image = forms.ImageField(required=False)

      class Meta:
            model = User
            fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

      def save(self, commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            if commit == True:
                  user.save()
                  Student.objects.create(
                        user=user, 
                        phone=self.cleaned_data['phone'],
                        country=self.cleaned_data['country'], 
                        image=self.cleaned_data['image'],
                        account_no = 100000 + user.id,
                  )
            return user
      
class StudentProfileForm(forms.ModelForm):
      class Meta:
            model = Student
            fields = ['phone', 'country', 'account_no', 'balance', 'image']
            
            # additional fields for User Model
            first_name = forms.CharField(max_length=30, required=True)
            last_name = forms.CharField(max_length=30, required=True)
            
            def __init__(self, *args, **kwargs):
                  super().__init__(*args, **kwargs)
                  
                  readonly_fields = ['account_no', 'balance', 'user__username', 'user__email']
                  
                  for field in readonly.fields:
                        self.fields[field].widget.attrs['readonly'] = True
                  
                  if self.instance.user:
                        self.fields['first_name'].initial = self.instance.user.first_name
                        self.fields['last_name'].initial = self.instance.user.last_name