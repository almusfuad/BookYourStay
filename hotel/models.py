from django.db import models
from student.models import Student
from django.utils.text import slugify



# Create your models here.
class Facilities(models.Model):
      name = models.CharField(max_length=50)
      def __str__(self):
            return self.name

class Hotel(models.Model):
      name = models.CharField(max_length=50)
      address = models.CharField(max_length=100)
      facilities = models.ManyToManyField(Facilities, related_name='hotels')
      image = models.ImageField(upload_to='hotel/media/image', blank=True)
      price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
      slug = models.SlugField(null=True, blank=True, unique=True)
      
      def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
      
      def __str__(self):
            return self.name
      
      
class Review(models.Model):
      RATING_CHOICES = [
        ("*", '1 star'),
        ("**", '2 stars'),
        ("***", '3 stars'),
        ("****", '4 stars'),
        ("*****", '5 stars'),
    ]
      hotel = models.ForeignKey(Hotel, related_name='reviews', on_delete=models.CASCADE)
      student = models.ForeignKey(Student, related_name='reviews', on_delete=models.CASCADE)
      rating = models.CharField(choices=RATING_CHOICES, max_length=15)
      review = models.TextField()
      slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)
      
      def save(self, *args, **kwargs):
            if not self.slug:
                  self.slug = slugify(f"{self.hotel.name}-{self.student.user.username}")
            super().save(*args, **kwargs)
      
      def __str__(self):
            return self.hotel.name + ' - ' + self.student.user.username