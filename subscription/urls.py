from django.urls import path
from . import views

urlpatterns = [
      path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
      
]