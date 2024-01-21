from django import forms
from . models import Review

class ReviewForm(forms.ModelForm):
      class Meta:
            model = Review
            fields = ['student','rating', 'review']

      def __init__(self, user, *args, **kwargs):
            super(ReviewForm, self).__init__(*args, **kwargs)
            self.fields['student'].initial = user  

      def set_hotel_field(self, hotel_instance):
            self.fields['hotel'].initial = hotel_instance