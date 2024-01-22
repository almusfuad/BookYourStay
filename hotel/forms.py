from django import forms
from . models import Review

class ReviewForm(forms.ModelForm):
      class Meta:
            model = Review
            fields = ['rating', 'review']
            widgets = {
                  'rating': forms.Select(choices=Review.RATING_CHOICES),
                  'review': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            }

      def __init__(self, user, *args, **kwargs):
            super().__init__(*args, **kwargs) 

      def set_hotel_field(self, hotel_instance):
            self.fields['hotel'].initial = hotel_instance