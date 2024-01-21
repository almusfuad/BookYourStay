from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
      path('register/', views.RegistrationView.as_view(), name = 'register'),
      path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
      path('login/', views.CustomLoginView.as_view(), name = 'login'),
      path('logout/', views.custom_logout, name = 'logout'),
      path('profile/', views.ProfileUpdateView.as_view(), name = 'profile'),
]