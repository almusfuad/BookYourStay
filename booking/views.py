from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from . models import Booking
from . forms import BookingForm
from django.urls import reverse_lazy
from transaction.models import Transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hotel.models import Hotel
from student.models import Student
from django.urls import reverse

# Create your views here.
class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hotel_slug = self.kwargs.get('hotel_slug')
        context['hotel_slug'] = hotel_slug
        return context

    def form_valid(self, form):
        hotel = self.get_hotel()
        user = self.request.user
        
        student, created = Student.objects.get_or_create(user=user)
        
        form.instance.hotel = hotel
        form.instance.student = student

        booking_amount = hotel.price


        if student.balance >= booking_amount:
            student.balance -= booking_amount
            student.save()

            Transaction.objects.create(student=student, amount=booking_amount, status='B')

            messages.success(self.request, 'Booking successful.')
            
            
            email_subject = 'Booking Confirmation'
            email_body = render_to_string('email/booking_confirmation.html', {'booking': form.instance})
            email = EmailMultiAlternatives(email_subject, email_body, to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            return redirect('hotel:home')

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['hotel_id'] = self.kwargs.get('hotel_id')
        return kwargs

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You need to be logged in.')
            return redirect(reverse_lazy('student:login'))
        return super().get(request, *args, **kwargs)

    def get_hotel(self):
        hotel_slug = self.kwargs.get('hotel_slug')
        return get_object_or_404(Hotel, slug=hotel_slug)