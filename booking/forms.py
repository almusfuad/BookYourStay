from django import forms
from . models import Booking

class BookingForm(forms.ModelForm):
      class Meta:
            model = Booking
            fields = ['arrival_date', 'departure_date', 'room_type', 'no_of_guests']
            widgets = {
                  'arrival_date': forms.DateInput(attrs={'type': 'date'}),
                  'departure_date': forms.DateInput(attrs={'type': 'date'}),
            }

      def __init__(self, *args, **kwargs):
        hotel_id = kwargs.pop('hotel_id', None)
        super(BookingForm, self).__init__(*args, **kwargs)