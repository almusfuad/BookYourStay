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
            return context


@method_decorator(login_required, name = 'dispatch')     
class ReviewCreateView(CreateView):
      model =  Review
      form_class = ReviewForm
      template_name = 'hotel/hotel_details.html'
      
      
      def get_success_url(self):
            return reverse_lazy('hotel:review_create', kwargs={'hotel_id': self.object.hotel.id, 'student_id': self.object.student.id})
      
      def form_valid(self, form):
            hotel_id = self.kwargs.get('hotel_id')
            student_id = self.kwargs.get('student_id')
            
            hotel_instance = get_object_or_404(hotel, id = hotel_id)
            student_instance = get_object_or_404(student, id = student_id)
            
            if Booking.objects.filter(hotel = hotel_instance, student=self.request.user).exists():
                  form.instance.hotel = hotel_instance
                  form.instance.student = student_instance
                  return super().form_valid(form)
            else:
                  messages.error(self.request, 'You can only review hotels you have booked.')
                  return self.form_invalid(form)
                  
            
      
      def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['user'] = self.request.user
            return Kwargs
      

@method_decorator(login_required, name = 'dispatch')      
class ReviewUpdateView(UpdateView):
      model = Review
      form_class = ReviewForm
      template_name = 'hotel/hotel_details.html'
      
      def get_success_url(self):
            return reverse_lazy('hotel:review_update', kwargs={'pk': self.object.id, 'hotel_id': self.object.hotel.id, 'student_id': self.object.student.id})
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["is_author"] = self.object.student == self.request.user
            return context
      
      def form_valid(self, form):
            hotel_instance = self.object.hotel
            student_instance = self.object.student

            if self.object.student == self.request.user and Booking.objects.filter(hotel = hotel_instance, student = self.request.user).exists():
                  return super().form_valid(form)
            else:
                  message.error(self.request, 'You are not the owner of the comment.')
                  return self.form_invalid(form)

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