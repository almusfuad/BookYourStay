from django.db import models
from student.models import Student
from hotel.models import Hotel

# Create your models here.
class Booking(models.Model):
      hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
      student = models.ForeignKey(Student, on_delete=models.CASCADE)
      arrival_date = models.DateField()
      departure_date = models.DateField()
      room_type = models.CharField(choices=(('S', 'Single'), ('D', 'Double'), ('F', 'Family')), max_length=10)
      no_of_guests = models.IntegerField()
      
      def __str__(self):
            return self.hotel.name + ' - ' + self.student.user.username