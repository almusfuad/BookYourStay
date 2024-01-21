from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Student
from .forms import RegistrationForm, StudentProfileForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# displaying messages
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
            student = Student.objects.create(
                  user = user,
                  phone = form.cleaned_data['phone'],
                  country = form.cleaned_data['country'],
                  image = form.cleaned_data['image'],
                  account_no = 10000 + user.id,
            )
            

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
            
            messages.success(self.request, 'Account created successfully. Please check your email for activation.')
            return redirect('student:login')

      def form_invalid(self, form):
            messages.error(self.request, 'Account creation failed. Please check your forms.')
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
            messages.success(request, "Account activated successfully. You can now log in.")
            return redirect('student:login')
      else:
            messages.error(request, 'Activation failed. Redirecting to registration.')
            # print("Activation failed. Redirecting to registration.")
            return redirect('student:register')
      
      
class CustomLoginView(LoginView):
      template_name = 'student/login.html'
      
      def get_success_url(self):
            messages.success(self.request, 'Login successful.')
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

@login_required 
def custom_logout(request):
      if request.method == "GET":
            logout(request)
            messages.success(request, 'Logout successful.')
            return redirect('student:login') 

#     # Handle GET requests if needed
#     return redirect('student:login')


@method_decorator(login_required, name = 'dispatch') 
class ProfileUpdateView(UpdateView):
      model = Student
      form_class = StudentProfileForm
      template_name = 'student/profile.html'
      success_url = reverse_lazy('student:profile')

      def get_object(self, queryset=None):
            return self.request.user.student

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['student'] = self.request.user.student
            context['update'] = self.get_object()
            return context

      def form_valid(self, form):
            form.instance.user = self.request.user
            messages.success(self.request, 'Profile updated successfully.')
            return super().form_valid(form)

      def form_invalid(self, form):
            messages.error(self.request, 'Profile update failed. Please check your forms.')
            return super().form_invalid(form)