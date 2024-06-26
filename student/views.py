from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetConfirmView
from .models import Student
from booking.models import Booking
from .forms import RegistrationForm, StudentUpdateForm, CustomUserChangeForm
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
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

# password reset email settings
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import Http404, HttpRequest

# Create your views here.
class RegistrationView(CreateView):
      model = Student
      form_class = RegistrationForm
      template_name = 'student/register.html'
      success_url = reverse_lazy('student:login')
      
      def post(self, request, *args, **kwargs):
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                  return self.form_valid(form)
            else:
                  #TODO: handle invalid form errorsS
                  return self.form_invalid(form)

      def form_valid(self, form):
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
                  
            # print(password1, password2)
            phone=form.cleaned_data['phone']
            country=form.cleaned_data['country']
            image=form.cleaned_data['image']
                  
            print(f'image: {image}, phone: {phone}, country: {country}')
                  
            if password1 != password2:
                  messages.error(self.request, 'Passwords do not match.')
                  return self.form_invalid(form)
                  
            user = form.save(commit=False)
            user.is_active = False
            user.save()
                  
            # create student instance
            student = Student.objects.create(
                  user=user, 
                  phone=phone,
                  country=country, 
                  image=image,
                  account_no = 100000 + user.id,
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
                  for error in form.errors:
                        messages.error(self.request, f'Account creation failed. {error}')
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
      
      
      
      def form_valid(self, form):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # print(password)
            messages.success(self.request, 'Login successful.')
            return super().form_valid(form)
      
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

@login_required 
def custom_logout(request):
      if request.method == "GET":
            logout(request)
            messages.success(request, 'Logout successful.')
            return redirect('student:login') 

#     # Handle GET requests if needed
#     return redirect('student:login')

@login_required
def student_info(request):
      try:
            student = Student.objects.get(user = request.user)
            bookings = Booking.objects.filter(student = student)
      except Student.DoesNotExist:
            raise Http404("Student does not exist")
      
      return render(request, 'student/profile.html', {'student': student, 'bookings': bookings})



@login_required
def update_info(request):
      if request.method == 'POST':
            user_form = CustomUserChangeForm(request.POST, instance=request.user)
            student_form = StudentUpdateForm(request.POST, request.FILES, instance=request.user.student)
            
            if user_form.is_valid() and student_form.is_valid():
                  user_form.save()
                  student_form.save()
                  messages.success(request, 'Your profile has been updated successfully.')
            else:
                  error_messages = "\n".join([f"{field}: {', '.join(errors)}" for field, errors in user_form.errors.items()])
                  messages.error(request, 'Your profile update failed.')
                  print(error_messages)
      else:
            messages.error(request, 'Invalid request method for profile update.')

      return redirect('student:profile')


@login_required
def custom_password_change(request):
      if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            
            if form.is_valid():
                  user = form.save()
                  update_session_auth_hash(request, user)
                  messages.success(request, 'Your password has been updated successfully.')
                  return redirect('student:profile')
            else:
                  messages.error(request, "Password don't match!")
      else:
            form = PasswordChangeForm(request.user)           
      return render(request,'student/profile.html', {'form': form})


UserModel = get_user_model()

def get_domain_name(request: HttpRequest) -> str:
      return request.get_host()

def custom_password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # If user with provided email doesn't exist, still display success message
                messages.success(request, 'Password reset email sent. Please check your inbox.')
                return redirect('student:login')
            
            # Generate a password reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            # Construct the password reset link
            reset_link = request.build_absolute_uri(
                reverse_lazy('student:password_reset_confirm', args=[uid, token])
            )
            
            # Sending email
            email_subject = 'Password Reset Request'
            email_body = render_to_string('email/password_reset_email.html', {'reset_link': reset_link})
            email = EmailMultiAlternatives(email_subject, email_body, to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            
            messages.success(request, 'Password reset email sent. Please check your inbox.')
            return redirect('student:login')
    else:
        form = PasswordResetForm()
    return render(request, 'student/password_reset_form.html', {'form': form})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
      template_name = 'student/password_reset_confirm.html'

      def form_valid(self, form):
            user = form.save()
            
            user = authenticate(username = user.username, password = form.cleaned_data['new_password1'])
            
            if user is not None:
                  login(self.request, user)
                  messages.success(self.request, 'Password has been reset successfully.')
                  return redirect('student:profile')
            else:
                  messages.error(self.request, 'Password reset failed.')
                  return redirect('student:login')
            

      def form_invalid(self, form):
            messages.error(self.request, 'Password reset link is invalid or has expired.')
            return redirect('student:login')