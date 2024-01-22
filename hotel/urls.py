from django.urls import path
from .views import HotelListView, HotelDetailsView

app_name = 'hotel'
urlpatterns = [
      path('', HotelListView.as_view(), name = 'home'),
      path('hotel/<slug:slug>/', HotelDetailsView.as_view(), name = 'hotel_detail'),
]