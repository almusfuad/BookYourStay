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
            context['user_has_booked'] = Booking.objects.filter(hotel=hotel, student = self.request.user.student).exists()
            return context


@method_decorator(login_required, name = 'dispatch')     
class ReviewCreateView(CreateView):
      model =  Review
      form_class = ReviewForm
      template_name = 'hotel/hotel_details.html'
      success_url = reverse_lazy("hotel:home")
      
      
      def form_valid(self, form):
            hotel_id = self.kwargs.get('hotel_id')
            student_id = self.kwargs.get('student_id')
            print('Checking')
            
            rating = form.cleaned_data['rating']  # Corrected this line
            review = form.cleaned_data['review']  # Corrected this line
            
            hotel_instance = get_object_or_404(Hotel, id=hotel_id)
            student_instance = get_object_or_404(Student, id=student_id)
            
            if Booking.objects.filter(hotel=hotel_instance, student=self.request.user.student).exists():
                  form.instance.hotel = hotel_instance
                  form.instance.student = student_instance
                  review_instance = form.save()  # Use form.save() to save the instance
                        
                  print(review_instance)
                  
                  self.object = review_instance
                  messages.success(self.request, 'Review submitted successfully.')
                  return super().form_valid(form)
            else:
                  messages.error(self.request, 'You can only review hotels you have booked.')
                  return self.form_invalid(form)
            
      def form_invalid(self, form):
            messages.error(self.request, 'Error submitting the review. Please check your input.')
            return super().form_invalid(form)    
      
        
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            hotel_id = self.kwargs.get('hotel_id')
            hotel_instance = get_object_or_404(Hotel, id = hotel_id)
            user = self.request.user
            student = Student.objects.get(user = user)
            context['student'] = student
            context['hotel'] = hotel_instance
            context['user_has_booked'] = Booking.objects.filter(hotel=hotel_instance, student = user.student).exists()
            return context
      
      def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['user'] = self.request.user
            return kwargs
      
      def get_success_url(self):
            return reverse_lazy('hotel:hotel_detail', kwargs={'slug': self.object.hotel.slug})

# def create_review(request, hotel_id):
#       print('Hitting review')
#       student = get_object_or_404(Student, user = request.user)
#       hotel = get_object_or_404(Hotel, id = hotel_id)
#       # booking = Booking.objects.filter(hotel=hotel_id, student=student)
#       reviews = get_object_or_404(Review, hotel=hotel)
#       form = ReviewForm()
#       if request.method == 'POST':
#             form = ReviewForm(request.POST)
#             if form.is_valid():
#                   # rating = form.cleaned_data['rating']
#                   # review = form.cleaned_data['review']
#                   review = form.save(commit=False)
#                   hotel = get_object_or_404(Hotel, id = hotel_id)
#                   # student = get_object_or_404(Student, id = student_id)
#                   review.hotel = hotel
#                   review.student = student
#                   review.save()
                  
#             reviews = get_object_or_404(Review, hotel=hotel)
#             return render(request, 'hotel_details.html', {'reviews': reviews, 'hotel': hotel, 'form': form, 'user_has_booked': True})
#       else:
#             return render(request, 'hotel_details.html', {'reviews': reviews, 'hotel': hotel, 'form': form, 'user_has_booked': True})
                                
            
      
      

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
            