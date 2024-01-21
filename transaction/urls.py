from django.urls import path
from . import views


app_name = 'transaction'

urlpatterns = [
      path('deposit/', views.DepositCreateView.as_view(), name='deposit'),
]