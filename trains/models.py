from django.db import models

# Create your models here.

class Train(models.Model):
    train_number = models.CharField(max_length=20, unique=True)
    train_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()

    def __str__(self):
        return f"{self.train_name} ({self.train_number})"