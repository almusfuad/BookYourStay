from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
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
from django.core.exceptions import ValidationError

# email
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Create your views here.
class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_form.html'
    success_url = reverse_lazy('hotel:home')

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
        no_of_guests = form.cleaned_data['no_of_guests']

        booking_amount = hotel.price


        if student.balance >= booking_amount:
            student.balance -= booking_amount
            student.save()
            
            form.save()

            Transaction.objects.create(student=student, amount=booking_amount, status='B')

            email_subject = 'Booking Confirmation'
            email_body = render_to_string('email/booking_confirmation.html', {'booking': form.instance})
            email = EmailMultiAlternatives(email_subject, email_body, to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            messages.success(self.request, 'Booking successful.')
            return redirect('hotel:home')
        else:
            messages.error(self.request, 'Insufficient balance. Please add funds to your account.')
            form.add_error(None, 'Insufficient balance. Please add funds to your account.')
            return self.render_to_response(self.get_context_data(form=form))
    
    def form_invalid(self, form):
        messages.error(self.request, 'Insufficient balance. Please add funds to your account.')

        return redirect('hotel:home')

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
    
    
    def cancel_booking(request, booking_id):
        booking = get_object_or_404(Booking, id = booking_id)
        
        if booking.arrival_date > timezone.now().date():
            if not booking.is_check_out and not booking.is_cancel:
                booking.is_cancel = True
                booking.save()
                
                request.user.student.balance += hotel.price
                
                Transaction.objects.create(
                    student = request.user.student,
                    amount = booking.hotel.price,
                    type = 'R',
                )
        return redirect('student:profile')