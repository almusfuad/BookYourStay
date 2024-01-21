from django.db import models
from student.models import Student

# Create your models here.
class Transaction(models.Model):
      student = models.ForeignKey(Student, on_delete=models.CASCADE)
      amount = models.DecimalField(max_digits=10, decimal_places=2)
      date = models.DateField(auto_now_add=True)
      status = models.CharField(choices=(('D', 'Deposit'), ('B', 'Booking')), max_length=10)
      
      def __str__(self):
            return self.student.user.username + ' - ' + str(self.amount)