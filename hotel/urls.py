from django.urls import path
from .views import HotelListView, HotelDetailsView, ReviewUpdateView, ReviewListView, ReviewCreateView

app_name = 'hotel'
urlpatterns = [
      path('', HotelListView.as_view(), name = 'home'),
      path('hotel/<slug:slug>/', HotelDetailsView.as_view(), name = 'hotel_detail'),
      # path('hotel/<int:hotel_id>/review', create_review, name= 'hotel_detail'),
      path('hotel/<int:hotel_id>/student/<int:student_id>/review/create', ReviewCreateView.as_view(), name = 'review-create'),
      path('hotel/<int:hotel_id>/student/<int:student_id>/review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
      path('reviews/', ReviewListView.as_view(), name='review_list'),
]