from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Student
from .forms import RegistrationForm, StudentProfileForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# activation Email
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Create your views here.
class RegistrationView(CreateView):
      model = Student
      form_class = RegistrationForm
      template_name = 'student/register.html'
      success_url = reverse_lazy('student:login')

      def form_valid(self, form):
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            # create student instance
            # student = Student.objects.create(
            #       user = user,
            #       phone = form.cleaned_data['phone'],
            #       country = form.cleaned_data['country'],
            #       image = form.cleaned_data['image'],
            #       account_no = 10000 + user.id,
            # )
            

            # generate token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = self.request.build_absolute_uri(
                  reverse_lazy('student:activate', args=[uid, token])
            )
            

            # sending email
            email_subject = 'Confirm Email'
            email_body = render_to_string('email/confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, email_body, to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            

            return redirect('student:login')

      def form_invalid(self, form):
            return render(self.request, 'student/register.html', {'form': form})
      
def activate(request, uid64, token):
      try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User._default_manager.get(pk=uid)
      except User.DoesNotExist:
            user = None

      if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            print(f"Account activated successfully for user: {user.username}")
            return redirect('student:login')
      else:
            print("Activation failed. Redirecting to registration.")
            return redirect('student:register')
      
      
class CustomLoginView(LoginView):
      template_name = 'student/login.html'
      
      def get_success_url(self):
            return reverse_lazy('hotel:home')
      
      # def form_valid(self, form):
      #       response = super().form_valid(form)
      #       user = 
      #             # checking user authentication before creating a token
      #             if user.is_authenticated:
      #                   token, _ = Token.objects.create(user=user)
      #                   response.set_cookie('token', token.key)
      #                   return HttpResponseRedirect(self.get_success_url())
      #             else:
      #                   logger.error("User authentication failed after login.")
      #       else:
      #             logger.error("User is not active.")      
            
      #       return response
      
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        
        return redirect('student:login') 

    # Handle GET requests if needed
    return redirect('student:login')


def profile_details(request):
      profile = Student.objects.get(user = request.user)
      return render(request, 'student/profile.html', {'profile': profile})

def profile_edit(request):
      profile = Student.objects.get(user = request.user)
      if request.method == 'POST':
            form = StudentProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                  form.save()
      else:
            form = StudentProfileForm(instance=profile)
                  
      return render(request, 'profile.html', {'form': form})