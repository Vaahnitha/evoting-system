from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user model (employees + admins)
class User(AbstractUser):
    role = models.CharField(max_length=20, default="employee")

    def __str__(self):
        return self.username


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, null=True, blank=True)
    #image = models.ImageField(upload_to='candidates/', null=True, blank=True)

    def __str__(self):
        return self.name


class Vote(models.Model):
    voter = models.OneToOneField(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.voter} voted for {self.candidate}"
