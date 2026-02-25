from django.db import models
from django.conf import settings
from trains.models import Train

# Create your models here.

class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    train = models.ForeignKey(
        Train,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    seats_booked = models.PositiveIntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.train.train_number}"