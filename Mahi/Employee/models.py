from django.db import models

# Create your models here.


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    profile_picture = models.ImageField(upload_to='pictures', blank=True, null=True)

    def __str__(self):
       return f"{self.first_name} {self.last_name}"
