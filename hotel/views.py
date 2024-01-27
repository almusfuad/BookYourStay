from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import CreateView
from . models import Hotel, Review
from booking.models import Booking
from student.models import Student
from . forms import ReviewForm, EditReviewForm
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

# Create your views here.
class HotelListView(ListView):
      model = Hotel
      template_name = 'hotel/home.html'
      context_object_name = 'hotels'
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['reviews'] = Review.objects.all()
            return context
      
class HotelDetailsView(DetailView):
      model = Hotel
      template_name = 'hotel/hotel_details.html'
      context_object_name = 'hotel'
      slug_field = 'slug'
      slug_url_kwarg = 'slug'
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            hotel = self.get_object()
            
            
            if self.request.user.is_authenticated:
                  student = self.request.user.student
                  context['user_has_booked'] = Booking.objects.filter(hotel=hotel, student = student).exists()   
                  context['review_owner'] = Review.objects.filter(hotel=hotel, student=student).exists()     # with exists() we get the boolean value
                  
                  context['edit_reviews'] = Review.objects.filter(hotel=hotel, student=student)
                  print(Review.objects.filter(hotel=hotel, student=student))
                  context['review_form'] = ReviewForm(user = self.request.user)
            context['reviews'] = Review.objects.filter(hotel = hotel)
            return context
      
      def post(self, request, *args, **kwargs):
            review_form = ReviewForm(user = request.user, data = self.request.POST, )
            hotel_instance = self.get_object()
            
            rating = request.POST.get('rating')
            review = request.POST.get('review')
            
            print(rating, review)
            
            if review_form.is_valid():
                  print('form is valid')
                  student_instance = Student.objects.get(user = request.user)
                  
                  if Booking.objects.filter(hotel = hotel_instance, student = student_instance).exists():
                        review_instance = Review.objects.create(
                                          hotel=hotel_instance,
                                          student=student_instance,
                                          rating=rating,
                                          review=review,
                                    )
                        
                        messages.success(request, 'Review submitted successfully.')
                        return redirect('hotel:hotel_detail', slug = hotel_instance.slug)
                  else:
                        print('cannot make it')
                        return redirect('hotel:hotel_detail', slug = hotel_instance.slug)
            else:
                  print('form is not valid')
                  print(review_form.errors)
                  messages.error(request, 'Error submitting the review. Please check your input.')
                  return redirect('hotel:hotel_detail', slug = hotel_instance.slug)
  
  
                        
# TODO: Make a class based view where user can edit, update and delete review which is owned by them

@login_required
def edit_review(request, slug):
      review = get_object_or_404(Review, slug=slug)
      
      if request.method == 'POST':
            form = EditReviewForm(request.POST, instance=review)
            if form.is_valid():
                  form.save()
                  messages.success(request, 'Your review has been updated.')
            else:
                  messages.error(request, 'Your review has not been updated.')
                  
      return redirect('hotel:hotel_detail', slug = review.hotel.slug)


@login_required
def delete_review(request, slug):
      review = get_object_or_404(Review, slug=slug)
      
      # check user permissions
      if request.user == review.student.user:
            review.delete()
            messages.success(request, 'Your review has been deleted.')
      else:
            messages.error(request, 'You do not have permission to delete this review.')
      
      return redirect('hotel:hotel_detail', slug = review.hotel.slug)