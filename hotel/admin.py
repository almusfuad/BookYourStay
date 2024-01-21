from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Facilities)
admin.site.register(models.Hotel)
admin.site.register(models.Review)