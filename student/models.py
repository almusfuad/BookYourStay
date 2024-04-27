from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Student(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      phone = models.CharField(max_length=15)
      country = models.CharField(max_length=50)
      account_no = models.IntegerField()
      balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
      image = models.ImageField(upload_to='student/media/images', null=True, blank=True)
      slug = models.SlugField(blank=True, null=True, max_length=100)
      
      USERNAME_FIELD = 'user__username'
      def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug based on username
            self.slug = slugify(self.user.username)

        super().save(*args, **kwargs)
      
      def __str__(self):
            return f'{self.account_no}'
