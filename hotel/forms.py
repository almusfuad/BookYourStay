from django import forms
from . models import Review

class ReviewForm(forms.ModelForm):
      class Meta:
            model = Review
            fields = ['rating', 'review']
            widgets = {
                  'rating': forms.Select(),
                  'review': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            }

      def __init__(self, user, *args, **kwargs):
            print('print after init in forms.py')
            super().__init__(*args, **kwargs)
            self.user = user  # storing user for letter use
            self.fields['rating'].choices = Review.RATING_CHOICES

      def set_hotel_field(self, hotel_instance):
            self.fields['hotel'].initial = hotel_instance
            
      def save(self, commit = False):
            print('print after save in forms.py')
            review = super().save(commit = False)
            review.hotel = self.fields['hotel'].initial
            review.student = self.user.student
            if commit:
                  review.save()
            return review
      
      def clean(self):
            print('print after clean in forms.py')
            cleaned_data = super().clean()
            return cleaned_data
      
      
class EditReviewForm(forms.ModelForm):
      class Meta:
            model = Review
            fields = ['rating', 'review']
            widgets = {
                  'rating': forms.Select(attrs={'class': 'form-control p-2'}),
                  'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            }