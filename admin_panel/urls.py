from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
      path('dashboard/', views.admin_dashboard, name='admin-dashboard'),
      path('edit_profile/', views.admin_profile, name='admin-profile'),
      path('password_update/', views.admin_password, name='admin-password'),
      path('logout/', views.admin_logout, name = 'admin-logout'),
]