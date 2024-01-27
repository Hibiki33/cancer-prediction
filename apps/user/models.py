from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Identity(models.TextChoices):
        Admin = 'A', 'Admin'
        Patient = 'P', 'Patient'
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    username = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    identity = models.CharField(max_length=1, choices=Identity.choices, default=Identity.Patient)
    