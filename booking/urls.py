from django.urls import path
from .views import BookingCreateView

app_name = 'booking'

urlpatterns = [
      path('create/<slug:hotel_slug>/', BookingCreateView.as_view(), name='booking-create'),
]