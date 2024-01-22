from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from . models import Hotel, Review
from booking.models import Booking
from student.models import Student
from . forms import ReviewForm
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
            
            context['reviews'] = Review.objects.filter(hotel = hotel)
            context['user_has_booked'] = Booking.objects.filter(hotel=hotel, student = self.request.user.student).exists()
            context['review_form'] = ReviewForm(user = self.request.user)
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
                        
      

@method_decorator(login_required, name = 'dispatch')      
class ReviewUpdateView(UpdateView):
      model = Review
      form_class = ReviewForm
      template_name = 'hotel/hotel_details.html'
      
      def get_success_url(self):
            return reverse_lazy('hotel:hotel_detail', kwargs={'slug': self.object.hotel.slug})
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["is_author"] = self.object.student == self.request.user
            return context
      
      def form_valid(self, form):
            hotel_instance = self.object.hotel
            student_instance = self.object.student

            if self.object.student == self.request.user and Booking.objects.filter(hotel = hotel_instance, student = self.request.user).exists():
                  messages.success(self.request, 'Review successfully submitted.')
                  return super().form_valid(form)
            else:
                  message.error(self.request, 'You are not the owner of the comment.')
                  return self.form_invalid(form)

      def form_invalid(self, form):
            messages.error(self.request, 'Error updating the review. Please check your input.')
            return super().form_invalid(form)
      
      
# @method_decorator(login_required, name='dispatch')
# class ReviewDeleteView(DeleteView):
      model = Review
      template_name = 'hotel/review_confirm_delete.html'  # You may need to create a separate template for confirmation
      success_url = reverse_lazy('home')

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['is_author'] = self.object.student == self.request.user
            return context

      def delete(self, request, *args, **kwargs):
            self.object = self.get_object()
            if self.object.student == self.request.user and Booking.objects.filter(hotel=self.object.hotel, student=self.request.user).exists():
                  return super().delete(request, *args, **kwargs)
            else:
                  messages.error(self.request, 'You are not the owner of the comment.')
                  return redirect('home') 


class ReviewListView(ListView):
    model = Review
    context_object_name = 'reviews'
    
    
class BookingDetails(ListView):
      model = Booking
      context_object_name = 'bookings'
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['bookings'] = Booking.objects.filter(student=self.request.user.student, hotel=self.request.hotel)
            return context
            