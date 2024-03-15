from django.db import models
from ..user.models import User


# Create your models here.

class Case(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)


class Image(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    image = models.ImageField(upload_to='images/')
    case = models.ForeignKey(Case, on_delete=models.CASCADE)

class FileChunk(models.Model):
    file_hash = models.CharField(max_length=255)
    chunk_hash = models.CharField(max_length=255)
    index = models.IntegerField()
    filename = models.CharField(max_length=255)
    size = models.IntegerField()
    chunk = models.FileField(upload_to='chunks/')
