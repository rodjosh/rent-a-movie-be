from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=100)
    img = models.CharField(max_length=500)
    description = models.TextField()

    def __str__(self):
        return self.title


class Rent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
