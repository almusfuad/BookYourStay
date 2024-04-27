from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
      path('register/', views.RegistrationView.as_view(), name = 'register'),
      path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
      path('login/', views.CustomLoginView.as_view(), name = 'login'),
      path('logout/', views.custom_logout, name = 'logout'),
      path('profile/', views.student_info, name = 'profile'),
      path('update_info/', views.update_info, name = 'update_info'),
      path('change_password/', views.custom_password_change, name = 'change_password'),
      path('password_reset/', views.custom_password_reset_request, name='password_reset_request'),
      path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
      # path('reset_done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),  # Add this line
]