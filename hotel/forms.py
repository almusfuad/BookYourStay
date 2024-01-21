from django import forms
from . models import Review

class ReviewForm(forms.ModelForm):
      class Meta:
            model = Review
            fields = ['rating', 'review']

      def __init__(self, user, *args, **kwargs):
            super(ReviewForm, self).__init__(*args, **kwargs)
            self.fields['student'].initial = user  # You can keep this line if you want to set an initial value
            # Remove the line below to enable editing of the 'student' field
            # self.fields['student'].widget.attrs['readonly'] = True

      def set_hotel_field(self, hotel_instance):
            self.fields['hotel'].initial = hotel_instance