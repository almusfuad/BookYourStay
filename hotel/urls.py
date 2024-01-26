from django.urls import path
from .views import HotelListView, HotelDetailsView, edit_review, delete_review

app_name = 'hotel'
urlpatterns = [
      path('', HotelListView.as_view(), name = 'home'),
      path('hotel/<slug:slug>/', HotelDetailsView.as_view(), name = 'hotel_detail'),
      path('edit_review/<slug:slug>/', edit_review, name = 'edit_review'),
      path('delete_review/<slug:slug>/', delete_review, name = 'delete_review'),
]